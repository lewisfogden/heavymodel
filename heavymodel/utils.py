class Cache:
  def __init__(self, func, param_len):
    self.func = func
    self.param_len = param_len
    self.has_one_param = self.param_len == 1
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
