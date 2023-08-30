import torch
from torch import nn


class AdaptiveConcatPool2d(nn.Module):
    def __init__(self):
        super().__init__()
        self.ap = nn.AdaptiveAvgPool2d((1, 1))
        self.mp = nn.AdaptiveMaxPool2d((1, 1))

    def forward(self, x): return torch.cat([self.mp(x), self.ap(x)], 1)


class Flatten(nn.Module):
    def __init__(self): super().__init__()

    def forward(self, x): return x.view(x.size(0), -1)


def remake_base_model(m):
    return nn.Sequential(m[0], nn.Sequential(*([AdaptiveConcatPool2d(), Flatten()] + list(m[1].children())[2:])))
