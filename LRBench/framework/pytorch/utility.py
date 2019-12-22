#!/bin/python

"""
Another option is to use torch.optim.lr_scheduler.LambdaLR
"""

def update_learning_rate(optimizer, lr):
    for param_group in optimizer.param_groups:
        param_group['lr'] = lr