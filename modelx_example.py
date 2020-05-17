"""
Example from here:
https://docs.modelx.io/en/latest/tutorial/api_tutorial.html#creating-the-life-space

model, life = new_model(), new_space('Life')

def l(x):
    if x == x0:
        return 100000
    else:
        return l(x - 1) - d(x - 1)

def d(x):
    return l(x) * q

def q():
    return 0.003

l, d, q = defcells(l, d, q)
life.x0 = 50

>>> life.frame
                   l           d      q
x
 50.0  100000.000000  300.000000    NaN
 51.0   99700.000000  299.100000    NaN
 52.0   99400.900000  298.202700    NaN
 53.0   99102.697300  297.308092    NaN
 54.0   98805.389208  296.416168    NaN
 55.0   98508.973040  295.526919    NaN
 56.0   98213.446121  294.640338    NaN
 57.0   97918.805783  293.756417    NaN
 58.0   97625.049366  292.875148    NaN
 59.0   97332.174218  291.996523    NaN
 60.0   97040.177695         NaN    NaN
NaN              NaN         NaN  0.003
"""

from heavymodel import Model

class Life(Model):
    def age(self, t):
        if t == 0:
            return self.x0
        else:
            return self.age(t-1) + 1

    def l(self, t):
        if self.age(t) == self.x0:
            return 100000
        else:
            return self.l(t-1) - self.d(t-1)
    
    def d(self, t):
        return self.l(t) * self.q

life = Life(data={"x0":50, "q":0.003})

life._run(100)

print(life._dataframe())
