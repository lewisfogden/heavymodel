# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 21:34:22 2020

@author: user
"""

# code call counting

from collections import defaultdict

class Count:
  def __init__(self, func):
    self.func = func
    self.call_count = defaultdict(int)
    self.__name__ = "counter: "+func.__name__

  def __call__(self, t):
    self.call_count[t] += 1
    result  = self.func(t)
    return result


class DecreasingModel:
    def value(self, t):
        if t==0:
            return 1
        else:
            return self.value(t-1) * 0.95
        
decreaser = DecreasingModel()
decreaser.value = Count(decreaser.value)
results = {}
for t in range(0,11):
    results[t] = decreaser.value(t)

print(results)

print(decreaser.value.call_count)