import torch
import torch.nn as nn
from model.common import FullyConnectedLayer
from model.common import DeConvLayer

class Render(torch.nn.Module):
    """ Neural network for rendering module of O2P2
    """

    def __init__(self):
        super(Render, self).__init__()

        # TODO: magic numbers in this class will be fixed

        wi = 14
        wh = 14

        self.image_fc = FullyConnectedLayer(256, 50176)

        self.image_deconv1 = DeConvLayer(256, 128, 5, 2, 2, 1)
        wi = self.image_deconv1.output_size(wi)

        self.image_deconv2 = DeConvLayer(128, 64, 5, 2, 2, 1)
        wi = self.image_deconv2.output_size(wi)

        self.image_deconv3 = DeConvLayer(64, 32, 6, 2, 2, 0)
        wi = self.image_deconv3.output_size(wi)

        self.image_deconv4 = DeConvLayer(32, 3, 6, 2, 2, 0)
        wi = self.image_deconv4.output_size(wi)

        self.f_image = nn.Sequential(self.image_deconv1, self.image_deconv2, self.image_deconv3, self.image_deconv4)

        self.heatmap_fc = FullyConnectedLayer(256, 50176)

        self.heatmap_softmax = nn.Softmax(1)

        self.heatmap_deconv1 = DeConvLayer(256, 128, 5, 2, 2, 1)
        wh = self.heatmap_deconv1.output_size(wh)

        self.heatmap_deconv2 = DeConvLayer(128, 64, 5, 2, 2, 1)
        wh = self.heatmap_deconv2.output_size(wh)

        self.heatmap_deconv3 = DeConvLayer(64, 32, 6, 2, 2, 0)
        wh = self.heatmap_deconv3.output_size(wh)

        self.heatmap_deconv4 = DeConvLayer(32, 1, 6, 2, 2, 0)
        wh = self.heatmap_deconv4.output_size(wh)

        self.f_heatmap = nn.Sequential(self.heatmap_deconv1, self.heatmap_deconv2, self.heatmap_deconv3, self.heatmap_deconv4)

        self.output_size = wh * wh * 3

    def forward(self, objs):
        images = []
        heatmaps = []

        for i, obj in enumerate(objs):
            i = self.image_fc(obj)
            i = i.view(-1, 256, 14, 14)
            i = self.f_image(i)
            images.append(i)

            h = self.heatmap_fc(obj)
            h = h.view(-1, 256, 14, 14)
            h = -self.f_heatmap(h)
            h = h.unsqueeze(1)
            heatmaps.append(h)

        w = torch.cat(heatmaps, 1)
        w = self.heatmap_softmax(w)
        w = w.transpose(0, 1)

        image = torch.zeros(w.shape[1], 3, 224, 224).cuda()
        for idx, i in enumerate(images):
            image += w[idx] * i

        return image
