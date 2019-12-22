from .LR import LR
from .LRfunctions import getLRFunction
from ..utility import trimLRparamStr

class piecewiseLR(LR):
    def __init__(self, _subRegions, _LRparams):
        self.subRegions = _subRegions
        self.LRparams = _LRparams
        self.LRfunctions = list()
        if len(self.subRegions) >= len(self.LRparams):
            raise Exception("LR policy error! the length of the sub-regions should be less than the LR parameters")
        for lrParam in self.LRparams:
            self.LRfunctions.append(getLRFunction(**lrParam))
        self.curStep = 0
        self.lastBoundary = 0
    def getLR(self, _iteration, _startIteration = 0):
        if self.curStep < len(self.subRegions) and _iteration >= self.subRegions[self.curStep]:
            self.lastBoundary = self.subRegions[self.curStep]
            self.curStep += 1
        return self.LRfunctions[self.curStep](_iteration-self.lastBoundary-_startIteration)
    def toString(self):
        return trimLRparamStr(str(self.LRparams)+'-AT-'+str(self.subRegions))
