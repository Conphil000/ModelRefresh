# -*- coding: utf-8 -*-
"""
Created on Sun May 22 17:22:55 2022

@author: Conor
"""

import pandas as pd
import json
import random
from threading import Thread
import time
# What do we need??

# We have a REST API running in the background. It has a model object instantiated.


class model:
    '''
    This is a ML Model;
    '''
    def __init__(self,uid):
        self._uid = uid
    def get_prediction(self,):
        return {f'model_{self._uid}':random.random()}      


class new_model:
    '''
    This is a ML Model;
    '''
    def __init__(self,uid):
        self._uid = uid
    def get_prediction(self,):
        return {f'model_{self._uid}':random.randint(1,100)}      

def set_refresh_False():
    with open('JSON/refreshed.json','w') as outfile:
        outfile.write(json.dumps(False))
def set_refresh_True():
    with open('JSON/refreshed.json','w') as outfile:
        outfile.write(json.dumps(True))
def check_refreshed():
    with open('JSON/refreshed.json','r') as openfile:
        return json.load(openfile)
    

t1 = time.time()
set_refresh_False()
v = check_refreshed() # takes like .00000003 s
t2 = time.time()
print(t2-t1)

FX = {}
FX['m1'] = model('1')
FX['m2'] = model('2')

class serviceRequest:
    def __init__(self,FX):
        self._services = FX
        self._current_model = 'm1'
        self._score_count = 0
    def update_model(self,):
        print('Model has been refreshed, starting new model in 30.\n')
        # two models:
        if self._current_model == 'm1':
            self._services['m2'] = new_model(2)
            new_id = 'm2'
        else:
            self._services['m1'] = model(1)
            new_id = 'm1'
            
        time.sleep(15)
        print('Change done.')
        new_thread = Thread(target = flip)
        new_thread.start()
        # Might need to lock _current_model object.
        self._current_model = new_id
        
    def get_current_score(self,):
        if check_refreshed():
            set_refresh_False()
            new_thread = Thread(target=self.update_model)
            new_thread.start()
        print(self._current_model,self._services[self._current_model].get_prediction())
        
obj = serviceRequest(FX)

def flip():
    print('flip in 15')
    time.sleep(15)
    set_refresh_True()
    print('flip done.')

new_thread = Thread(target = flip)
new_thread.start()

import numpy as np
for i in np.arange(0,500):
    obj.get_current_score()
    time.sleep(0.25)




