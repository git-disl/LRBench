# this module provides utility functions for LRBench

# temporary solution
import re
def trimLRparamStr(s):
    return s.replace(' ', '').replace('\'', '').replace('[', '').replace(']', '').replace('{', '').replace('},', '-').replace('}', '').replace(':', '_').replace(',', '+')

def _parseLRValue(value):
    if value == 'None' or len(value) < 1:
        return None
    if str.isalpha(value[0]):
        return value
    elif '.' in value or 'e' in value:
        return float(value)
    else:
        return int(value)

def parseLRStr(s):
    result = dict()
    params = re.split("(?<=[^e])\+", s)
    lList = list()
    i = 0
    while i < len(params):
        name, value = params[i].split("_")
        i+=1
        if name == 'l':
            while i < len(params) and "_" not in params[i]:
                lList.append(int(params[i]))
                i+=1
            if len(lList) == 0:
                result[name] = _parseLRValue(value)
            else:
                lList.insert(0, _parseLRValue(value))
                result[name] = lList
        else:
            result[name] = _parseLRValue(value)
    return result

def buildLRsFromStr(s):
    from LR import LR
    from fixedPiecewiseLR import fixedPiecewiseLR
    from piecewiseLR import piecewiseLR
    if '-AT-' not in s: # Parse a Single LR
        return LR(parseLRStr(s))
    if '-k0F-' not in s: # Parse Piecewise LR
        LRparams, regions = s.split('-AT-')
        # regions
        regionResult = list()
        for r in re.split("(?<=[^e])\+", regions):
            regionResult.append(int(r))
        LRparamResult = list()
        for lr in re.split("(?<=[^e])-", LRparams):
            LRparamResult.append(parseLRStr(lr))
        return piecewiseLR(regionResult, LRparamResult)
    else: # Parse fixedPiecewiseLR
        LRparams, remains = s.split('-AT-')
        LRparamResult = list()
        for lr in re.split("(?<=[^e])-", LRparams):
            LRparamResult.append(parseLRStr(lr))
        regionSize, remains = remains.split('-k0F-')
        k0F, remains = remains.split('-k1F-')
        k1F, lF = remains.split('-lF-')
        if k1F == "None":
            k1F = None
        else:
            k1F = float(k1F)
        if lF == "None":
            lF = None
        else:
            lF = float(lF)
        return fixedPiecewiseLR(int(regionSize), LRparamResult, float(k0F), k1F, lF)
        
# Module Test
if __name__=='__main__':
    testStr = "k1_0.006+k0_0.001+lrPolicy_UPCOS+l_2000"
    print(parseLRStr(testStr))