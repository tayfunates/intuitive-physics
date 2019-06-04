import argparse
import os
from util import filesystem


class BaseOptions:
    """This class defines options used during both training and test time.
    """
    def __init__(self):
        """Reset the class
        """
        self.initialized = False
        self.parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    def initialize(self):
        self.parser.add_argument('--name', type=str, default='experiment_name',
                                 help='name of the experiment. It decides where to store samples and models')
        self.parser.add_argument('--checkpoints_dir', type=str, default='./checkpoints',
                                 help='models are saved here')
        self.parser.add_argument('--dataroot', default='./datasets/PhysVQA',
                                 help='path to images (should have subfolders first, last, mask, segment)')
        self.parser.add_argument('--train_batch_size', type=int, default=1, help='training batch size')
        self.parser.add_argument('--test_batch_size', type=int, default=1, help='test batch size')
        self.parser.add_argument('--max-epoch', default=120, type=int, help="maximum epochs to run")
        self.parser.add_argument('--eval-freq', default=10, type=int, help="evaluation frequency")
        self.parser.add_argument('--seed', type=int, default=23, help='random seed')
        self.parser.add_argument('--use-perceptual-loss', action='store_true',
                                 help="use perceptual loss in addition to L2 loss")
        self.initialized = True
        
    def get_options(self):
        """ Initialize the parser with user options (only once)
        """
        if not self.initialized:  # check if it has been initialized
            self.initialize()
            
        opts = self.parser.parse_args()
        return opts
        
    def print_options(self, opt):
        """Print and save options
        It will print both current options and default values(if different).
        It will save options into a text file / [checkpoints_dir] / opt.txt
        """
        message = ''
        message += '----------------- Options ---------------\n'
        for k, v in sorted(vars(opt).items()):
            comment = ''
            default = self.parser.get_default(k)
            if v != default:
                comment = '\t[default: %s]' % str(default)
            message += '{:>25}: {:<30}{}\n'.format(str(k), str(v), comment)
        message += '----------------- End -------------------'
        print(message)

        # save to the disk
        expr_dir = os.path.join(opt.checkpoints_dir, opt.name)
        filesystem.mkdir(expr_dir)
        file_name = os.path.join(expr_dir, "_opt.txt")
        with open(file_name, 'wt') as opt_file:
            opt_file.write(message)
            opt_file.write('\n')
            
    def parse(self):
        """Parse our options, create checkpoints directory suffix, and set up gpu device."""
        opt = self.get_options()

        self.print_options(opt)

        return opt
