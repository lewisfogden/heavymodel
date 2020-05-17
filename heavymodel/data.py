# -*- coding: utf-8 -*-

class Data:
    def __init__(self, d):
        seqs = tuple, list, set, frozenset
        for i, j in d.items():
            if isinstance(j, dict):
                setattr(self, i, Data(j))
            elif isinstance(j, seqs):
                setattr(self, i, type(j)(Data(sj) if isinstance(sj, dict) else sj for sj in j))
            else:
                setattr(self, i, j)
    def _copy(self):
        return self.__copy__()
    
    def __copy__(self):
        return Data(self.__dict__.copy())
    
    def __repr__(self):
        return "<Data " + repr(self.__dict__) + ">"
    
    def __iter__(self):
        return iter(self.__dict__)