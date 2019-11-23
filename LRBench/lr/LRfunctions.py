from functools import partial
import math

def __FIX__(iter, k0):
    return k0 #k0 * iter / iter

def __STEP__(iter, k0, gamma, l):
    return k0*(gamma**(math.floor(iter/l)))

def __NSTEP__(iter, k0, gamma, l): # Be careful when using this LR
    if __NSTEP__.curStep < len(l) and iter >= l[__NSTEP__.curStep]:
        __NSTEP__.curStep += 1
        #print("Next Step at " + str(iter) + " iterations, at step: " + str(__NSTEP__.curStep))
    return k0*(gamma**__NSTEP__.curStep)

def __EXP__(iter, k0, gamma):
    return k0 * (gamma**iter)

def __INV__(iter, k0, gamma, p):
    return k0*((1+gamma*iter)**(-p))

def __POLY__(iter, k0, k1, p, l):
    return (k1-k0)*((1.0-1.0*iter/l)**p) + k0

def __SIG__(iter, k0, gamma, l):
    return k0*1.0/(1+math.exp(-1.0*gamma*(iter-l)))

#CLR family
def __TRI__(iter, k0, k1, l):
    period = 2 * l
    return (k1-k0)*(2/math.pi)*math.fabs(math.asin(math.sin(math.pi*iter/(period)))) + k0

def __DTRI__(iter, k0, k1, l):
    period = 2.0 * l
    return (k1-k0)*(2/math.pi)*math.fabs(math.asin(math.sin(math.pi*((iter+l)/period)))) + k0

def __TRI2__(iter, k0, k1, l):
    period = 2 * l
    return (k1-k0)*(2/math.pi)*math.fabs(math.asin(math.sin(math.pi*iter/(period))))/(2**math.floor(iter/period)) + k0

def __DTRI2__(iter, k0, k1, l):
    period = 2 * l
    return (k1-k0)*(2/math.pi)*math.fabs(math.asin(math.sin(math.pi*(iter+l)/(period))))/(2**math.floor((iter+l)/period)) + k0

def __TRIEXP__(iter, k0, k1, gamma, l):
    period = 2 * l
    return (k1-k0)*(2/math.pi)*math.fabs(math.asin(math.sin(math.pi*iter/(period))))*(gamma**iter) + k0

def __DTRIEXP__(iter, k0, k1, gamma, l):
    period = 2 * l
    return (k1-k0)*(2/math.pi)*math.fabs(math.asin(math.sin(math.pi*(iter+l)/(period))))*(gamma**iter) + k0

def __SIN__(iter, k0, k1, l):
    period = 2 * l
    return (k1-k0)*math.fabs(math.sin(math.pi*iter/period)) + k0

def __DSIN__(iter, k0, k1, l):
    period = 2 * l
    return (k1-k0)*math.fabs(math.sin(math.pi*(iter+l)/period)) + k0

def __SIN2__(iter, k0, k1, l):
    period = 2 * l
    return (k1-k0)*math.fabs(math.sin(math.pi*iter/period))/(2**math.floor(iter/period)) + k0

def __DSIN2__(iter, k0, k1, l):
    period = 2 * l
    return (k1-k0)*math.fabs(math.sin(math.pi*(iter+l)/period))/(2**math.floor((iter+l)/period)) + k0

def __SINEXP__(iter, k0, k1, gamma, l):
    period = 2 * l
    return (k1-k0)*math.fabs(math.sin(math.pi*iter/period))*(gamma**iter) + k0

def __DSINEXP__(iter, k0, k1, gamma, l):
    period = 2 * l
    return (k1-k0)*math.fabs(math.sin(math.pi*(iter+l)/period))*(gamma**iter) + k0

def __COS__(iter, k0, k1, l):
    return (k1 - k0) * 0.5 * (1+math.cos(math.pi *iter / l)) + k0

def __UPCOS__(iter, k0, k1, l):
    return (k1 - k0) * 0.5 * (1+math.cos(math.pi * (1.0*iter / l + 1.0))) + k0

def __COS2__(iter, k0, k1, l):
    return (k1 - k0) * 0.5 * (1+math.cos(math.pi *iter / l))/(2**math.floor((iter+l)/(2*l))) + k0

def __UPCOS2__(iter, k0, k1, l):
    return (k1 - k0) * 0.5 * (1+math.cos(math.pi * (1.0*iter / l + 1.0)))/(2**math.floor((iter)/(2*l))) + k0

def __COSEXP__(iter, k0, k1, gamma, l):
    return (k1 - k0) * 0.5 * (1+math.cos(math.pi *iter / l))*(gamma**iter) + k0

def __UPCOSEXP__(iter, k0, k1, gamma, l):
    return (k1 - k0) * 0.5 * (1+math.cos(math.pi * (1.0*iter / l + 1.0)))*(gamma**iter) + k0

# Restart family

def __RSW__(iter, k0, k1, l):
    return (k1 - k0) * (-1.0*iter/l - math.floor(-1.0*iter/l)) + k0

def __RSW2__(iter, k0, k1, l):
    return (k1 - k0) * (-1.0*iter/l - math.floor(-1.0*iter/l))/(2**math.floor(1.0*iter/l)) + k0

def __RSWEXP__(iter, k0, k1, gamma, l):
    return (k1 - k0) * (-1.0*iter/l - math.floor(-1.0*iter/l))*(gamma**iter) + k0

def __SINRSW__(iter, k0, k1, l):
    return (k1 - k0) * math.sin(math.pi/2.0*(-1.0*iter/l - math.floor(-1.0*iter/l))) + k0

def __SINRSW2__(iter, k0, k1, l):
    return (k1 - k0) * math.sin(math.pi/2.0*(-1.0*iter/l - math.floor(-1.0*iter/l)))/(2**math.floor(1.0*iter/l)) + k0

def __SINRSWEXP__(iter, k0, k1, gamma, l):
    return (k1 - k0) * math.sin(math.pi/2.0*(-1.0*iter/l - math.floor(-1.0*iter/l)))*(gamma**iter) + k0

def __COSRSW__(iter, k0, k1, l):
    return (k1 - k0) * 0.5 * (1 - math.cos(math.pi*(-1.0*iter/l - math.floor(-1.0*iter/l)))) + k0

def __COSRSW2__(iter, k0, k1, l):
    return (k1 - k0) * 0.5 * (1 - math.cos(math.pi*(-1.0*iter/l - math.floor(-1.0*iter/l))))/(2**math.floor(1.0*iter/l)) + k0

def __COSRSWEXP__(iter, k0, k1, gamma, l):
    return (k1 - k0) * 0.5 * (1 - math.cos(math.pi*(-1.0*iter/l - math.floor(-1.0*iter/l))))*(gamma**iter) + k0

def getLRFunction(lrPolicy, k0, k1=None, gamma=None, p=None, l=None):
    if lrPolicy == 'FIX':
        return partial(__FIX__, k0=k0)
    elif lrPolicy == 'STEP':
        return partial(__STEP__, k0=k0, gamma=gamma, l=l)
    elif lrPolicy == 'NSTEP':
        __NSTEP__.curStep = 0 # Be careful with this initialization. Do not call getLRFunction(p)(), each time it will initialize it.
        return partial(__NSTEP__, k0=k0, gamma=gamma, l=l)
    elif lrPolicy == 'EXP':
        return partial(__EXP__, k0=k0, gamma=gamma)
    elif lrPolicy == 'INV':
        return partial(__INV__, k0=k0, gamma=gamma, p=p)
    elif lrPolicy == 'POLY':  # By default k_e = 0 for Caffe's implementation; TODO: Modify it to support k_e != 0
        return partial(__POLY__, k0=k0, k1=k1, p=p, l=l)
    elif lrPolicy == 'SIG':
        return partial(__SIG__, k0=k0, gamma=gamma, l=l)
    elif lrPolicy == 'TRI':
        return partial(__TRI__, k0=k0, k1=k1, l=l)
    elif lrPolicy == 'TRI2':
        return partial(__TRI2__, k0=k0, k1=k1, l=l)
    elif lrPolicy == 'TRIEXP':
        return partial(__TRIEXP__, k0=k0, k1=k1, gamma=gamma, l=l)
    elif lrPolicy == 'DTRI':
        return partial(__DTRI__, k0=k0, k1=k1, l=l)
    elif lrPolicy == 'DTRI2':
        return partial(__DTRI2__, k0=k0, k1=k1, l=l)
    elif lrPolicy == 'DTRIEXP':
        return partial(__DTRIEXP__, k0=k0, k1=k1, gamma=gamma, l=l)
    elif lrPolicy == 'SIN':
        return partial(__SIN__, k0=k0, k1=k1, l=l)
    elif lrPolicy == 'SIN2':
        return partial(__SIN2__, k0=k0, k1=k1, l=l)
    elif lrPolicy == 'SINEXP':
        return partial(__SINEXP__, k0=k0, k1=k1, gamma=gamma, l=l)
    elif lrPolicy == 'DSIN':
        return partial(__DSIN__, k0=k0, k1=k1, l=l)
    elif lrPolicy == 'DSIN2':
        return partial(__DSIN2__, k0=k0, k1=k1, l=l)
    elif lrPolicy == 'DSINEXP':
        return partial(__DSINEXP__, k0=k0, k1=k1, gamma=gamma, l=l)
    elif lrPolicy == 'COS':
        return partial(__COS__, k0=k0, k1=k1, l=l)
    elif lrPolicy == 'COS2':
        return partial(__COS2__, k0=k0, k1=k1, l=l)
    elif lrPolicy == 'COSEXP':
        return partial(__COSEXP__, k0=k0, k1=k1, gamma=gamma, l=l)
    elif lrPolicy == 'UPCOS':
        return partial(__UPCOS__, k0=k0, k1=k1, l=l)
    elif lrPolicy == 'UPCOS2':
        return partial(__UPCOS2__, k0=k0, k1=k1, l=l)
    elif lrPolicy == 'UPCOSEXP':
        return partial(__UPCOSEXP__, k0=k0, k1=k1, gamma=gamma, l=l)
    elif lrPolicy == 'RSW':
        return partial(__RSW__, k0=k0, k1=k1, l=l)
    elif lrPolicy == 'RSW2':
        return partial(__RSW2__, k0=k0, k1=k1, l=l)
    elif lrPolicy == 'RSWEXP':
        return partial(__RSWEXP__, k0=k0, k1=k1, gamma=gamma, l=l)
    elif lrPolicy == 'SINRSW':
        return partial(__SINRSW__, k0=k0, k1=k1, l=l)
    elif lrPolicy == 'SINRSW2':
        return partial(__SINRSW2__, k0=k0, k1=k1, l=l)
    elif lrPolicy == 'SINRSWEXP':
        return partial(__SINRSWEXP__, k0=k0, k1=k1, gamma=gamma, l=l)
    elif lrPolicy == 'COSRSW':
        return partial(__COSRSW__, k0=k0, k1=k1, l=l)
    elif lrPolicy == 'COSRSW2':
        return partial(__COSRSW2__, k0=k0, k1=k1, l=l)
    elif lrPolicy == 'COSRSWEXP':
        return partial(__COSRSWEXP__, k0=k0, k1=k1, gamma=gamma, l=l)
    else:
        raise Exception('Learning Rate lrPolicy not defined!')
