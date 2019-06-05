import torch
import torchvision
from torch.utils.data import DataLoader
from torchvision.transforms import *
import numpy as np
from options.options import BaseOptions
from util.logger import Logger
from util.filesystem import mkdir
from util.checkpoint import save_checkpoint
import os.path as osp
from data.PhysVQA import PhysVQA
from data.dataset import O2P2Dataset
from model.percept import Percept
from model.physics import Physics
from model.render import Render
from loss.vgg import Vgg16, Normalization
import time


def main():
    opt = BaseOptions().parse()   # get options
    exp_dir = osp.join(opt.checkpoints_dir, opt.name)
    log_file = osp.join(exp_dir, "trainlog.txt")
    logger = Logger(log_file)
    use_gpu = torch.cuda.is_available()
    torch.manual_seed(opt.seed)
    torch.cuda.manual_seed_all(opt.seed)

    # Read and initialize dataset
    phys_vqa_data = PhysVQA(opt.dataroot)

    # Construct train and test transform operations
    transform_train = Compose([
        ToTensor(),
    ])
    transform_test = Compose([
        ToTensor(),
    ])

    # PyTorch Dataset classes for train, validation and test sets
    train_dataset = O2P2Dataset(phys_vqa_data.train, phys_vqa_data.max_objects, transform=transform_train)
    val_dataset = O2P2Dataset(phys_vqa_data.val, phys_vqa_data.max_objects,  transform=transform_test)
    test_dataset = O2P2Dataset(phys_vqa_data.test, phys_vqa_data.max_objects, transform=transform_test)

    # PyTorch Dataloaders for train, validation and test sets
    train_loader = DataLoader(train_dataset, batch_size=opt.train_batch_size, shuffle=True, pin_memory=use_gpu)
    val_loader = DataLoader(val_dataset, batch_size=opt.test_batch_size, shuffle=False, pin_memory=use_gpu)
    test_loader = DataLoader(test_dataset, batch_size=opt.test_batch_size, shuffle=False, pin_memory=use_gpu)

    # Initialize model
    percept = Percept()
    physics = Physics()
    render = Render()
    if use_gpu:
        percept = percept.cuda()
        physics = physics.cuda()
        render = render.cuda()

    # Initialize pretrained vgg model for perceptual loss
    vgg = Vgg16(requires_grad=False)
    vgg.eval()
    if use_gpu:
        vgg = vgg.cuda()

    # VGG network expects images that are normalized with these mean and std
    vgg_normalization_mean = torch.tensor([0.485, 0.456, 0.406])
    vgg_normalization_std = torch.tensor([0.229, 0.224, 0.225])
    if use_gpu:
        vgg_normalization_mean = vgg_normalization_mean.cuda()
        vgg_normalization_std = vgg_normalization_std.cuda()

    # Initialize normalizer that is required by vgg model
    vgg_norm = Normalization(vgg_normalization_mean, vgg_normalization_std)
    if use_gpu:
        vgg_norm = vgg_norm.cuda()

    # Define loss and optimizers
    criterion = torch.nn.MSELoss()
    optim_percept = torch.optim.Adam(percept.parameters(), lr=1e-3)
    optim_physics = torch.optim.Adam(physics.parameters(), lr=1e-3)
    optim_render = torch.optim.Adam(render.parameters(), lr=1e-3)

    best_render_loss = np.inf
    best_epoch = 0
    print("==> Start training")

    # Start training
    for epoch in range(opt.max_epoch):
        start_time = time.time()

        # train for one epoch
        percept_loss, physics_loss, render_loss = train(epoch, train_loader, percept, physics, render, criterion,
                                                        vgg, vgg_norm, optim_percept, optim_physics, optim_render,
                                                        use_gpu, exp_dir, logger, opt)

        elapsed_time = time.time() - start_time

        # print training details
        print_train_stats(logger, epoch, elapsed_time, percept_loss, physics_loss, render_loss)

        if (epoch + 1) % opt.eval_freq == 0:
            percept_loss, physics_loss, render_loss = validate(epoch, val_loader, percept, physics, render, criterion,
                     vgg, vgg_norm, use_gpu, exp_dir, logger, opt)

            is_best = render_loss < best_render_loss
            if is_best:
                best_render_loss = render_loss
                best_epoch = epoch + 1

            percept_state_dict = percept.state_dict()
            physics_state_dict = physics.state_dict()
            render_state_dict = render.state_dict()
            save_checkpoint({
                'percept_state_dict': percept_state_dict,
                'physics_state_dict': physics_state_dict,
                'render_state_dict': render_state_dict,
                'epoch': epoch,
            }, is_best, osp.join(exp_dir, 'checkpoint_ep' + str(epoch + 1) + '.pth.tar'))

    logger.log("==> Best Render Loss {:.4%}, achieved at epoch {}".format(best_render_loss, best_epoch))
    logger.log("Training completed.")


def print_train_stats(logger, epoch, elapsed_time, percept_loss, physics_loss, render_loss):
    """ Prints training details
    """
    logger.log('Epoch: [{0}]\t'
               'Time {epoch_time:.1f}\t'    
               'Perception Loss {percept_loss:.4f}\t'
               'Physics Loss {physics_loss:.3f} \t' 
               'Rendering Loss {render_loss:.4f}\t\t'.format(
                    epoch+1, epoch_time=elapsed_time, percept_loss=percept_loss,
                    physics_loss=physics_loss, render_loss=render_loss))


def train(epoch, train_loader, percept, physics, render, criterion, vgg,
          vgg_norm, optim_percept, optim_physics, optim_render,
          use_gpu, exp_dir, logger, opt):
    """ Train the model for one epoch.
    """

    # switch to train mode
    percept.train()
    physics.train()
    render.train()

    percept_losses = []
    physics_losses = []
    render_losses = []

    for batch_idx, (img0, img1, segs) in enumerate(train_loader):
        if use_gpu:
            img0, img1, segs = img0.cuda(), img1.cuda(), segs.cuda()

        # compute model output
        objects = percept(segs)

        img0_reconstruction = render(objects)
        objects_evolved = physics(objects)
        img1_reconstruction = render(objects_evolved)

        # measure l2 losses
        percept_loss_l2 = criterion(img0, img0_reconstruction)
        physics_loss_l2 = criterion(img1, img1_reconstruction)

        if opt.use_perceptual_loss:
            # get vgg features for perceptual loss
            img0_vgg_features = vgg(vgg_norm(img0)).relu2_2
            img0_reconstruction_vgg_features = vgg(vgg_norm(img0_reconstruction)).relu2_2
            img1_vgg_features = vgg(vgg_norm(img1)).relu2_2
            img1_reconstruction_vgg_features = vgg(vgg_norm(img1_reconstruction)).relu2_2

            # measure perceptual losses
            percept_loss_perceptual = criterion(img0_vgg_features, img0_reconstruction_vgg_features)
            physics_loss_perceptual = criterion(img1_vgg_features, img1_reconstruction_vgg_features)
        else:
            percept_loss_perceptual = 0
            physics_loss_perceptual = 0

        # calculate final losses
        percept_loss = percept_loss_l2 + percept_loss_perceptual
        physics_loss = physics_loss_l2 + physics_loss_perceptual
        render_loss = percept_loss + physics_loss

        percept_losses.append(percept_loss)
        physics_losses.append(physics_loss)
        render_losses.append(render_loss)

        # compute gradient and do optimizer step for percept module
        optim_percept.zero_grad()
        percept_loss.backward(retain_graph=True)
        optim_percept.step()

        # compute gradient and do optimizer step for physics module
        optim_physics.zero_grad()
        physics_loss.backward(retain_graph=True)
        optim_physics.step()

        # compute gradient and do optimizer step for render module
        optim_render.zero_grad()
        render_loss.backward()
        optim_render.step()

        percept_loss = sum(percept_losses) / float(len(percept_losses))
        physics_loss = sum(physics_losses) / float(len(physics_losses))
        render_loss = sum(render_losses) / float(len(render_losses))

        print_freq = 10
        if (batch_idx + 1) % print_freq == 0:
            logger.log('Epoch: [{0}][{1}/{2}]\t'
                       'Perception Loss {percept_loss:.4f}\t'
                       'Physics Loss {physics_loss:.3f} \t'
                       'Rendering Loss {render_loss:.4f}\t\t'.format(
                        epoch+1, batch_idx + 1, len(train_loader),
                        percept_loss=percept_loss,
                        physics_loss=physics_loss,
                        render_loss=render_loss))

        # save training images of a scene from last batch of epoch, for qualitative analysis
        if (batch_idx + 1) == len(train_loader):
            img0_name = 'epoch{}_img0.png'.format(epoch+1, '03')
            img0_recon_name = 'epoch{}_img0_reconstruction.png'.format(epoch+1, '03')
            img1_name = 'epoch{}_img1.png'.format(epoch+1, '03')
            img1_recon_name = 'epoch{}_img1_reconstruction.png'.format(epoch+1, '03')
            train_images_dir = osp.join(exp_dir, "train_images")
            mkdir(train_images_dir)
            img0_path = osp.join(train_images_dir, img0_name)
            img0_recon_path = osp.join(train_images_dir, img0_recon_name)
            img1_path = osp.join(train_images_dir, img1_name)
            img1_recon_path = osp.join(train_images_dir, img1_recon_name)
            torchvision.utils.save_image(img0, img0_path)
            torchvision.utils.save_image(img0_reconstruction, img0_recon_path)
            torchvision.utils.save_image(img1, img1_path)
            torchvision.utils.save_image(img1_reconstruction, img1_recon_path)

    return percept_loss, physics_loss, render_loss


def validate(epoch, val_loader, percept, physics, render, criterion, vgg, vgg_norm, use_gpu, exp_dir, logger, opt):
    """ Validates the current model (with validation set).
    """

    # switch to evaluate mode
    percept.eval()
    physics.eval()
    render.eval()

    percept_losses = []
    physics_losses = []
    render_losses = []

    with torch.no_grad():
        for batch_idx, (img0, img1, segs) in enumerate(val_loader):
            if use_gpu:
                img0, img1, segs = img0.cuda(), img1.cuda(), segs.cuda()

            # compute model output
            # compute model output
            objects = percept(segs)

            img0_reconstruction = render(objects)
            objects_evolved = physics(objects)
            img1_reconstruction = render(objects_evolved)

            # measure l2 losses
            percept_loss_l2 = criterion(img0, img0_reconstruction)
            physics_loss_l2 = criterion(img1, img1_reconstruction)

            if opt.use_perceptual_loss:
                # get vgg features for perceptual loss
                img0_vgg_features = vgg(vgg_norm(img0)).relu2_2
                img0_reconstruction_vgg_features = vgg(vgg_norm(img0_reconstruction)).relu2_2
                img1_vgg_features = vgg(vgg_norm(img1)).relu2_2
                img1_reconstruction_vgg_features = vgg(vgg_norm(img1_reconstruction)).relu2_2

                # measure perceptual losses
                percept_loss_perceptual = criterion(img0_vgg_features, img0_reconstruction_vgg_features)
                physics_loss_perceptual = criterion(img1_vgg_features, img1_reconstruction_vgg_features)
            else:
                percept_loss_perceptual = 0
                physics_loss_perceptual = 0

            # calculate final losses
            percept_loss = percept_loss_l2 + percept_loss_perceptual
            physics_loss = physics_loss_l2 + physics_loss_perceptual
            render_loss = percept_loss + physics_loss

            # record losses
            percept_losses.append(percept_loss)
            physics_losses.append(physics_loss)
            render_losses.append(render_loss)

            # save validation images for qualitative analysis

            img0_name = 'val{}_img0.png'.format(batch_idx+1, '03')
            img0_recon_name = 'val{}_img0_reconstruction.png'.format(batch_idx + 1, '03')
            img1_name = 'val{}_img1.png'.format(batch_idx + 1, '03')
            img1_recon_name = 'val{}_img1_reconstruction.png'.format(batch_idx + 1, '03')
            val_images_dir = osp.join(exp_dir, "val_images_epoch_{}".format(epoch + 1))
            mkdir(val_images_dir)
            img0_path = osp.join(val_images_dir, img0_name)
            img0_recon_path = osp.join(val_images_dir, img0_recon_name)
            img1_path = osp.join(val_images_dir, img1_name)
            img1_recon_path = osp.join(val_images_dir, img1_recon_name)
            torchvision.utils.save_image(img0, img0_path)
            torchvision.utils.save_image(img0_reconstruction, img0_recon_path)
            torchvision.utils.save_image(img1, img1_path)
            torchvision.utils.save_image(img1_reconstruction, img1_recon_path)

    percept_loss = sum(percept_losses) / float(len(percept_losses))
    physics_loss = sum(physics_losses) / float(len(physics_losses))
    render_loss = sum(render_losses) / float(len(render_losses))

    logger.log('Epoch: [{0}]\t'
               'Perception Validation Loss {percept_loss:.4f}\t'
               'Physics Validation Loss {physics_loss:.3f} \t'
               'Rendering Validation Loss {render_loss:.4f}\t\t'.format(
                        epoch + 1,
                        percept_loss=percept_loss,
                        physics_loss=physics_loss,
                        render_loss=render_loss))

    return percept_loss, physics_loss, render_loss


if __name__ == '__main__':
    main()

