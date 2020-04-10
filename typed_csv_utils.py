# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 09:28:56 2020

@author: Lewis Fogden
"""

import decimal




class TypedCSV:
    def __init__(self, filename):
        # define row processors
        self.types = {
                "int": int,
                "float": float,
                "str": str,
                "bool": self.get_bool,
                "dec": decimal.Decimal,
                "yyyy_mm_dd": str,   #TODO: add date and time processing
                "hh_mm_ss": str
                }
        
        
        self.processors = {
            "@": self.process_meta,
            "#": self.process_comment,
            "!": self.process_header,
            "?": self.process_type,
            "*": self.process_data}
        
       
        # add defaults
        self.separator = ","
        self.expected_length = None
        self.md5sum = None
        self.meta = {}
        self.data = [] # stored as row-wise list of lists
        
        # process each line
        with open(filename, 'r') as file:
            for raw_line in file:
                raw_line = raw_line.strip("\n")
                char1 = raw_line[0]
                print(char1, raw_line)
                self.processors[char1](raw_line)

                #except KeyError:
                #    raise KeyError(f"{char1} is an invalid first character.")
        # Run Post Import Tests
        self.run_checks() # check md5-checksum and length if provided
                
    def process_meta(self, raw_line):
        if raw_line[0:2] == "@ ":
            line = raw_line[2:]
        else:
            line = raw_line[1:]
        key, value = line.split(":",1)
        print(key, value)
        if key == "length":
            self.expected_length = int(value)
        elif key == "separator":
            self.separator = value
        elif key == "md5-checksum":
            self.md5sum = value
        # store all metadata
        self.meta[key] = value
        
    def process_comment(self, raw_line):
        pass
    
    def process_header(self, raw_line):
        print(f"header: {raw_line}")
        self.header = raw_line.split(self.separator)[1:]
        print(self.header)
        
    def process_type(self, raw_line):
        print(f"types: {raw_line}")
        data_types = []
        type_list = raw_line.split(self.separator)[1:]
        print(type_list)
        for col in type_list:
            try:
                data_types.append(self.types[col])
            except KeyError:
                raise KeyError(f"Unsupported type '{col}' in types")
        self.data_types = data_types
        print(self.data_types)

    def process_data(self, raw_line):
        print(f"data: {raw_line}")
        data_strings = raw_line.split(self.separator)[1:]
        print(data_strings)
        typed_data = [data_type(data) for data_type, data in zip(self.data_types, data_strings)]
        self.data.append(typed_data)
    
    def get_bool(self, string):
        if string.lower() in ["y", "t", "true", "1"]:
            return True
        elif string.lower() in ["n", "f", "false", "0"]:
            return False
        else:
            raise KeyError(f"Invalid Boolean (bool): {string}")
    
    def yield_dict(self):
            """iterate over all rows, returning a dictionary of each row"""
            for row in self.data:
                yield {k:v for k,v in zip(self.header, row)}

    def run_checks(self):
        print("running checks")
        
    def __enter__(self):
        pass
    
    def __exit__(self):
        pass

if __name__ == '__main__':
    filename = r"D:\dev\heavymodel\models\data\test1.tcsv"
    tcsv = TypedCSV(filename)
    for row in tcsv.yield_dict():
        print(row)