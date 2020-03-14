# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 17:11:13 2019

@author: user
"""

# yaml data validation

yaml_str = """
    term_y:
        type: int
        validation:
             min: 10
             max: 30
              
    smoker_status:
        type: str
        validation:
           - S
           - N
"""

class Validation:
    pass

class ValidationError(KeyError):
    pass

class RangeItem(Validation):
    _type = "RangeItem"
    def __init__(self, type, min, max, step=1):
        self.type = type
        self.min = min
        self.max = max
    def get(self, value):
        val = self.type(value)
        if val < self.min:
            raise ValidationError("Value " + str(val) + " below minimum ("+str(self.min) + ").")
        elif val > self.max:
            raise ValidationError("Value " + str(val) + "above maximum ("+str(self.max) + ").")
        else:
            return val

class ListItem(Validation):
    _type = "ListItem"
    def __init__(self, type, seq):
        self.type = type
        self.seq = seq
    def get(self, value):
        val = self.type(value)
        if val in self.seq:
            return val
        else:
            raise ValidationError("Option " + str(val) + " not in seq: " + repr(self.seq) +".")


import yaml
 
data_dict = yaml.load(yaml_str, Loader=yaml.FullLoader)

def parse_data_dict(data_dict):
    schema = dict()
    for k, v in data_dict.items():
        if v["type"] in ["int, float"]:
            