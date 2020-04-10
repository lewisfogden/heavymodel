from .utils import Cache
import types
import warnings
from inspect import signature

class Model:
    """The Model class provides the core caching functionality required for a heavy model.

    Functions in a heavy model should not start with an underscore "_"

    functions are as follows:
    _update(data or basis item): adds data or basis to the model space
    _clear_cache()
    _run(proj_len)
    _dataframe()

    """

    def __init__(self, data=None, basis=None):
        if data is not None:
            self._update(data)

        if basis is not None:
            self._update(basis)

    def _update(self, items, warn=True):
        for k, v in vars(items).items():
            if k in dir(self) and warn:
                warnings.warn("Warning: Duplicate Item: "+str(k))
            setattr(self, k, v)

    def _cache_funcs(self):
        #print("Caching...")
        self._funcs = {}
        for k in dir(self):
            v = getattr(self, k)
            #print(k, v, isinstance(v, types.MethodType), isinstance(v, opus.utils.Cache))
            #if k[0] != "_" and callable(v) and not isinstance(v, opus.utils.Cache):
            if k[0] != "_" and isinstance(v, types.MethodType):
                v_params = signature(v).parameters # we need an identifier for the arg length.
                v_param_len = len(v_params)
                cached_v = Cache(v, v_param_len)
                setattr(self, k, cached_v)
                self._funcs[k] = cached_v
        #print("INFO: _cache_funcs | cached funcs: "+str(len(self._funcs)))

    def _clear_cache(self):
        #print("INFO: Clearing cache")
        for k in dir(self):
            v = getattr(self, k)
            try:
                v.clear_cache()
            except AttributeError:
                pass

    def _run(self, proj_len):
        self._clear_cache()
        self._cache_funcs()
        for t in range(proj_len):
            for var in self._funcs.keys():
                func = getattr(self, var)
                if func.has_one_param:   # skip functions with more than one parameter
                    func(t)   #call each function in turn, starting from t==0

    def _dataframe(self):
        import pandas as pd
        df = pd.DataFrame()
        for func in self._funcs:
            df[func] = pd.Series(self._funcs[func].values)
        return df
