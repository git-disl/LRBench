'''
This module requires tensorflow and keras.
'''

import tensorflow as tf 
from keras import backend
import numpy as np
from LRBench.lr.LRfunctions import getLRFunction 


class ChangeLROnPlateau(tf.keras.callbacks.Callback):   
    '''
    The ChangeLROnPlateau class is a custom callback for Keras models that adjusts the learning 
    rate dynamically based on the performance of the model on a validation set. It's designed to 
    reduce the learning rate when the model stops improving to help fine-tune the model. If the 
    model is on a plateau, the learning rate can be increased or decreased depending on 
    the stage of training. 

    parameter intro:
    
    LR_func_list: A list of learning rate functions. These functions are used to calculate the 
    new learning rate at the beginning of each training batch based on the current training 
    iteration. The functions are cycled through depending on the model's performance.

    start_index: The starting index in the LR_func_list. It refers to the function in the list 
    that will be used at the beginning of training to calculate the learning rate.

    cooldown: The number of epochs to wait before resuming normal operation after the learning 
    rate has been reduced. This is to prevent the callback from acting too quickly and reducing 
    the learning rate again before the model has a chance to react to the previous reduction.

    threshold: The threshold for measuring the new optimum. If the difference between the current 
    metric and the best metric from the past is less than the threshold, the model is considered 
    to be on a plateau.

    monitor: The quantity to be monitored, such as 'val_loss' or 'val_accuracy'. The callback uses 
    this metric to decide whether the model's performance has improved sufficiently.

    metric_detection_iter: The number of recent iterations to consider when determining if the 
    model is on a plateau. The callback looks at the performance metrics from the most 
    recent 'metric_detection_iter'(e.g. 5) iterations to make this decision.

    '''  
    def __init__(self, LR_func_list,start_index, cooldown=5, threshold=0.05,    
                 monitor='var_loss', metric_detection_iter=5): 
        super().__init__()  

        self.LR_func_list = LR_func_list
        self.current_index = start_index
        self.cooldown = cooldown 
        self.cooldown_count = 0 
        self.threshold = threshold
        self.monitor = monitor 
        self.metric_detection_iter = metric_detection_iter 
   
    def on_train_begin(self, logs=None): # clean cache and set monitor_op 
        if 'loss' in self.monitor:
            self.monitor_op = lambda a, b: np.less(max(np.diff(a[::-1])), b) 
            if 'val' in self.monitor: self.monitor = 'val_loss'
            else:                     self.monitor = 'loss'
        if 'acc' in self.monitor:
            self.monitor_op = lambda a, b: np.less(max(np.diff(a)), b) # the diff of acc      
            if 'val' in self.monitor: self.monitor = 'val_accuracy'
            else:                     self.monitor = 'accuracy' 
        
        self.total_iter = self.params['epochs'] * self.params['steps'] 
        self.metric_lst = []
        self.iter_lst = []
        self.action_lst = []
        self.lr_lst = []
        

    def on_train_batch_begin(self, batch, logs=None): # input new iter to get the new lr from current LR function  
        iter = int(self.model._train_counter) + 1
        new_lr = getLRFunction(**LR_func_list[self.current_index])(iter)
        backend.set_value(self.model.optimizer.lr, new_lr)
       
        self.iter_lst.append(iter)
        self.lr_lst.append(new_lr)


    def on_epoch_end(self, epoch, logs=None):  # choose the new LR function   
        current = logs.get(self.monitor)
        self.metric_lst.append(current) 
        
        action = self.is_trapped_on_plateau_action()  
        self.action_lst.append(action)

        if (action == 'increase') & (self.current_index>0):
            self.current_index -= 1
        elif (action == 'decrease') & (self.current_index<len(LR_func_list)-1):
            self.current_index += 1
        else:
            pass          
        

    def is_trapped_on_plateau_action(self): 
        if (self.is_trapped_on_plateau()) & (self.cooldown_count == 0):
            self.cooldown_count = self.cooldown
            if self.model._train_counter / self.total_iter < 0.8:   # increase when hit the threshold
                return 'increase'    
            else:                              # flip at the end of training, decrease when hit the threshold
                return 'decrease' 
        else:
            if self.cooldown_count > 0:
                self.cooldown_count -= 1
            return 'no action'               


    def is_trapped_on_plateau(self): 
        # loss metric: if the diff of loss_rev is smaller than threshold, the model is trapped on the plateau
        # acc metric: if the diff of acc is smaller than threshold, the model is trapped on the plateau
        if len(self.metric_lst)>self.metric_detection_iter:
            latest_n_metrics = self.metric_lst[-self.metric_detection_iter:]
            if self.monitor_op(latest_n_metrics, self.threshold):
                return True
            else:
                return False  
        else:
            return False    


    def get_monitor_result(self):
        return {'iteration': self.iter_lst, 
                'learning rate': self.lr_lst, 
                'action': self.action_lst, 
                'metric': self.metric_lst}
    
