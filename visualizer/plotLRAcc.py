import matplotlib
import numpy as np
import matplotlib.pyplot as plt
# optional for the publication requirement on the font type
#matplotlib.rcParams['ps.useafm'] = True
#matplotlib.rcParams['pdf.use14corefonts'] = True
#matplotlib.rcParams['text.usetex'] = True


def plotLRAcc(x_lr, y_acc, colors, y_acc_labels, lr_str='(FIX, k)'):
    # input x_lr, y_acc should be numpy arrays
    # y_acc: size: (len(colors or y_acc_labels), len(x_lr))
    recordN = y_acc.shape[0]
    plt.figure(figsize=(8.0, 6.0))
    plt.xlabel('Learning Rate ' + lr_str, fontsize = 18)
    plt.ylabel('Accuracy (\%)', fontsize = 18)
    for i in range(recordN-1, -1, -1):
        plt.plot(x_lr, 100*y_acc[i], colors[i], label=str(y_acc_label[i])+' Epoch(s)')
    plt.xscale('log')
    plt.legend(bbox_to_anchor=(0.732, 1.01), loc=2, fontsize = 12.5, handlelength=1)
    #plt.axvline(x=0.001, linestyle='dashed', color='k')
    #plt.axvline(x=0.0005, linestyle='dashed', color='r')
    #plt.axvline(x=0.006, linestyle='dashed', color='r')
    #plt.axvline(x=0.01, linestyle='dashed', color='k')
    #plt.axvline(x=0.0001, linestyle='dashed', color='k')
    plt.tick_params(axis='both', which='major', labelsize=15)
    plt.savefig('acc-lr.png')
    

# for module test
#if __name__=='__main__':