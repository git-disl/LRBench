# Abstract API for LRs

from .LRfunctions import getLRFunction
from ..utility import *

class LR(object):
    def __init__(self, _lrParam):
        self.lrParam = _lrParam
        self.LRfunction = getLRFunction(**self.lrParam)
        
    def getLR(self, _iteration, _startIteration=0):
        return self.LRfunction(_iteration-_startIteration)
    
    def toString(self):
        return trimLRparamStr(str(self.lrParam))