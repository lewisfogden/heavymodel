# Definitions

This page provides an implementation free definition of what each method does, along with an example


```python
class MyModel(Model):
    def func_a(self, t):
        if t == 0:
            return 1
        else:
            return func_a(t-1) - func_b(t-1) 
    def func_b(self, t):
        return self.rate * self.func_a(t)

model = MyModel(rate=0.05)
```
