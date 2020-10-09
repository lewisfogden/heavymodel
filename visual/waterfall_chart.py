# -*- coding: utf-8 -*-
"""
Created on Sun May 31 16:19:52 2020

@author: user
"""

import pandas as pd
import matplotlib.pyplot as plt

values  = [100, 110, 95, 85, 97, 108, 115]
markers = [True,  False,False,False ,False,False,True]
labels  = ["Start", "Investment", "Mortality", "Morbidity", "Inflation", "Expenses", "Lapse"]

# bar x, width
# bar start
# bar end
# bar colour
# bar spacing

df = pd.DataFrame({"values":values, "markers":markers, "labels":labels})

def waterfall_chart(values, markers, labels):
    """returns a figure containing a waterfall plot"""

colour_palette = {
        'up':"darkgreen",
        'down': "red",
        'abs': "darkblue"}

x = []
height = []
bottom = []
color = []
deltas = []
for i, (v, m, label)  in enumerate(zip(values, markers, labels)):
    print (i, v, m, label)
    x.append(label)
    if m:
        height.append(v)
        bottom.append(0)
        color.append(colour_palette["abs"])
        deltas.append(None)
        
    else:
        delta = values[i] - values[i-1]
        deltas.append(delta)
        if delta > 0:
            height.append(delta)
            bottom.append(values[i]-delta)
            color.append(colour_palette["up"])
        else:
            height.append(abs(delta))
            bottom.append(values[i])
            color.append(colour_palette["down"])
       
#x = labels
#height = values
#bottom = [v-10 for v in values]
plt.bar(x=x, height=height, bottom=bottom, color=color, width=0.6)

# annotate
for x, h, delta in zip(x, height, deltas):
    plt.annotate(str(delta), xy=(x,h))

plt.show()
    
    