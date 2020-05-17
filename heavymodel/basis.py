# -*- coding: utf-8 -*-

import yaml
from .tables import MortalityTable, YieldCurve

class Basis:
    def __init__(self, data_dict, flatten=True, load_all=True):
        # recurse through dictionary
        # check type of item
        # assign each item to a top level slot
        # 
        for k, v in data_dict.items():
            if k == "data":
                self._data = v
                # parse data
                # TODO: data should be a validation schema rather than actual values, Basis.import(data) to validate & insert.
                #for data_name, data_type in v.items():
                #    setattr(self, data_name, data_type)
                    
            elif k == "assumptions":
                for data_name, data_type in v.items():
                    setattr(self, data_name, self.process_item(data_type))

            elif k == "parameters":
                for data_name, data_type in v.items():
                    setattr(self, data_name, self.process_item(data_type))
                # parse parameters
            else:
                #print("WARNING: " + str(k) + " is not a valid top level configuration item, skipped.")
                pass
                
    def __repr__(self):
        return "<Basis items: " + str(len(self.__dict__)) + ">"
    
    def process_item(self, item):
        if isinstance(item, bool):
            return int(item)
        elif isinstance(item, (int, float, str)):
            return item
        elif isinstance(item, dict):
            if item["type"] == "mortality_table":
                return MortalityTable(csv_filename=item["filename"], name=item["filename"], select_period=item["select_period"], pc_of_base = item["pc_of_base"])
            elif item["type"] == "yield_curve":
                return YieldCurve(filename=item["filename"], key_period=item["key_period"], rate_type="spot_rate")
        else:
            raise KeyError(str(item) + " is of unknown type")
    
    def __setitem__(self, key, value):
        setattr(self, key, value)
    
    def copy(self):
        new_basis = Basis({})
        for k, v in self.__dict__.items():
            new_basis[k] = v
        return new_basis
    
    @staticmethod
    def read_yaml(filename):
        #root_path = os.path.dirname(__file__)
        #abs_filename = os.path.join(root_path, filename)
        with open(filename) as config_file:
            data = yaml.load(config_file, Loader=yaml.FullLoader)
            return Basis(data)