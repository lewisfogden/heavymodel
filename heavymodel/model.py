import types
import warnings
from inspect import signature

class Cache:
    """Cache provides controllable memoization for model methods"""

    def __init__(self, func, param_len):
        self.func = func
        self.param_len = param_len
        self.has_one_param = self.param_len == 1
        self.values = dict()
        self.__name__ = "Cache: " + func.__name__

    def __call__(self, *arg):
        if arg in self.values:
            return self.values[arg]
        else:
            result = self.func(*arg)
            self.values[arg] = result
            return result

    def __repr__(self):
        return (
            "<CFunction: "
            + str(self.func.__name__)
            + " size: "
            + str(len(self.values))
            + ">"
        )

    def clear_cache(self):
        self.values = dict()

class Model:
    """The Model class provides the core caching functionality required for a heavy model.

    User methods subsetting from Model should not start with an underscore "_"

    Built-in functions are as follows:
    _update(data or basis item): adds data or basis to the model space
    _clear_cache(): clears all stored values
    _run(proj_len): run
    _dataframe():

    """

    def __init__(self, data=None, basis=None):
        if data is not None:
            self._update(data)

        if basis is not None:
            self._update(basis)

    def _update(self, items, warn=True):
        if isinstance(items, dict):
            for k,v in items.items():
                if k in dir(self) and warn:
                   warnings.warn("Warning: Duplicate Item: "+str(k))
                setattr(self, k, v)
        else:
            # need to check that this is a data object
            for k, v in vars(items).items():
                if k in dir(self) and warn:
                    warnings.warn("Warning: Duplicate Item: "+str(k))
                setattr(self, k, v)

    def _cache_funcs(self, verbose=False):
        #print("Caching...")
        self._funcs = {}
        for method_name in dir(self):
            method = getattr(self, method_name)
            if verbose:
                print("Caching: ", method_name, " object: ", method)
            #if k[0] != "_" and callable(v) and not isinstance(v, opus.utils.Cache):
            if method_name[0] != "_" and isinstance(method, types.MethodType):
                param_count = len(signature(method).parameters) # we need an identifier for the arg length.
                cached_method = Cache(method, param_count)
                setattr(self, method_name, cached_method)
                self._funcs[method_name] = cached_method
        #print("INFO: _cache_funcs | cached funcs: "+str(len(self._funcs)))

    def _clear_cache(self):
        #print("INFO: Clearing cache")
        for k in dir(self):
            v = getattr(self, k)
            try:
                v.clear_cache()
            except AttributeError:
                pass

    def _run(self, proj_len, verbose=False):
        self._clear_cache()
        self._cache_funcs(verbose)
        for t in range(proj_len):
            for var in self._funcs.keys():
                func = getattr(self, var)
                if func.has_one_param:   # skip functions with more than one parameter
                    func(t)   #call each function in turn, starting from t==0

    def _dataframe(self):
        import pandas as pd
        df = pd.DataFrame()
        for func in self._funcs:
            if func.has_one_param:
                df[func] = pd.Series(self._funcs[func].values)
        return df
