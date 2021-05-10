#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 10 11:21:48 2021

@author: l3x
"""


import numpy as np
from sklearn.base import BaseEstimator

from scipy.optimize import minimize
from sklearn.model_selection import GridSearchCV


class TestRegressor(BaseEstimator):  
    """An example of classifier"""

    def __init__(self, param_a=0, param_b=0):
        """
        Called when initializing the classifier
        """
        self.param_a = param_a
        self.param_b = param_b


    def loss(self,arg):
        print(arg)
        return np.linalg.norm((self.fd_y-(arg[0]*self.fd_x+arg[1]))**2)

    def _model(self, x, params):
        output = params[0] * x + params[1]
        return output 

    def score(self,X,y):
        return self._loss(self._model(X,[self.param_a,self.param_b]),y)
    
    # 2. Define the loss function
    def _loss(self, y_obs, y_pred):
        """Compute the dealer gain
    
        :param np.array y_obs: real sales
        :param np.array y_pred: predicted sales = purchasses
        """
        return np.linalg.norm(y_obs - y_pred)

    # 3. Function to be minimized
    def _f(self, params, *args):
        """Function to minimize = losses for the dealer

        :param args: must contains in that order:
        - data to be fitted (pd.Series)
        - model (function)
        """
        x = self.x_train
        y_obs = self.y_train
        y_pred = self._model(x, params)
        l = self._loss(y_pred, y_obs)
        return l
    
    def fit(self, X, Y):
        """
        Fit global model on X features to minimize 
        a given function on Y.

        @param X: train dataset (features, N-dim)
        @param Y: train dataset (target, 1-dim)
        """
        self.x_train = X
        self.y_train = Y
        param_initial_values = [self.param_a,self.param_b]
        res = minimize(
            self._f,
            x0=param_initial_values, 
        )
        print("Optimization result:\n\n",res)
        self.param_a,self.param_b = res['x']
        return self
