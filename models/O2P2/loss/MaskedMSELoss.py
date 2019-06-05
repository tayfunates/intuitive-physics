import torch

class MaskedMSELoss(torch.nn.Module):
    def __init__(self, requires_grad=False):
        super(MaskedMSELoss, self).__init__()
        self.mseLoss = torch.nn.MSELoss(reduction='none')

    def forward(self, X, Y, M):
        out = self.mseLoss(X, Y)
        M = torch.unsqueeze(M, 1)
        out = torch.sum(out.mul(M)) / (torch.sum(M) * out.shape[1])
        return out