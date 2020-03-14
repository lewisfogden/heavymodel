import types

class Cache:
  def __init__(self, func):
    self.func = func
    self.values = dict()
    self.__name__ = "Cache: "+func.__name__

  def __call__(self, arg):
    if arg in self.values:
        return self.values[arg]
    else:
        result = self.func(arg)
        self.values[arg] = result
        return result
  def __repr__(self):
    return "<CFunction: "+str(self.func.__name__) + " size: "+str(len(self.values)) + ">"
    
  def clear_cache(self):
    self.values = dict()
 
def run(model, proj_len=None):
    clear_results(model)
    cache_model(model)
    return run_model(model, proj_len=proj_len, target_variables=None)
    
    
def cache_model(model):
    if not hasattr(model, "_funcs"):
        model._funcs = {}
    for k,v in vars(model).items():
        if isinstance(v, types.FunctionType):
            cached_func = Cache(v)
            vars(model)[k] = cached_func
            model._funcs[k] = cached_func
        else:
            pass
    
    return model._funcs
    
def run_model(model, proj_len, target_variables=None):
    # this avoids recursion depths issues, by evaluating target_variables for t in order, target_variables can include core functions (defaults to all)
    #print("Running Model:", model)
    
    if proj_len is None:
        proj_len = model.basis.proj_len

    if target_variables is None:
        target_variables = list(model._funcs.keys())
    
    model.basis.proj_len = proj_len
    for t in range(proj_len):
      for var in target_variables:
        getattr(model, var)(t)   #call each function in turn, starting from t==0
    return True
    

def clear_results(model):
    for k,v in vars(model).items():
        try:
            v.clear_cache()
        except AttributeError:
            pass

