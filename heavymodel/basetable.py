# -*- coding: utf-8 -*-

from collections import namedtuple as _namedtuple

class BaseTable:
    _field_types = {"str":str,
                    "int": int,
                    "float": float}
    
    def __init__(self, rows):
        self.rows = rows
    
    @staticmethod
    def from_csv(csv_filename):
        """This reads in an appropriately formatted csv file.
        The final column is the value, the other columns are keys"""
        
        with open(csv_filename, 'r') as csv_file:
            header = None
            rows = {}
            for line in csv_file:
                line = line.strip("\n").split(",")
                print(line)
                if header is None:
                    header = line[:-1]
                    fields = {i.split(":")[0]:i.split(":")[1] for i in line}
                    print(fields)
                    value_type = line[-1].split(":")[1]
                    print(f"{value_type}")
                    keys = _namedtuple("Keys", field_names=header)
                else:
                    key = keys(*line[:-1])
                    value = float(line[-1])
                    print("key: ", key)
                    print("value: ", value)
                    rows[key] = value
            return BaseTable(rows)
                
                    #read line into header and set keys and values
if __name__ == '__main__':
    ip06 = BaseTable.from_csv(r"D:\dev\heavymodel\models\tables\IP06_DP4.csv")