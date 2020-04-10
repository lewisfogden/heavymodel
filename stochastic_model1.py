# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 20:36:22 2020

@author: user
"""

from heavymodel import Model, Data

import random
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
sns.set()
rng = random.Random(0) # seed set to ensure replicable.

class Asset(Model):
    def asset_value(self, t):
        if t == 0:
            return 1
        else:
            return self.asset_value(t-1) * (1 + self.inv_growth(t))
    
    def inv_growth(self, t):
        return rng.normalvariate(self.mu, self.sigma)

class _Asset(Model):
    def _asset_value(self, t):
        if t == 0:
            return 1
        else:
            return self._asset_value(t-1) * (1 + self._inv_growth(t))
    
    def _inv_growth(self, t):
        return rng.normalvariate(self.mu, self.sigma)

def simAsset(runs=1000):
    results = []
    data = Data(dict(mu=0.04, sigma=0.13))
    for count, sim in enumerate(range(simulations)):
        asset = Asset(data=data)
        asset._run(121)
        results.append(asset.asset_value(120))
    return results

def sim_Asset(runs=1000):
    results = []
    data = Data(dict(mu=0.04, sigma=0.13))
    for count, sim in enumerate(range(simulations)):
        asset = _Asset(data=data)
        asset._run(121)
        results.append(asset._asset_value(120))
    return results

if __name__ == "__main__":
    data = Data(dict(mu=0.04, sigma=0.13))
    #am = Asset(data)
    #am._run(20)
    #print(am.asset_value.values)
    #am._dataframe().plot()
    
   
    simulations = 1000
    results = []
    print(f"Running {simulations} Simulations")
    for count, sim in enumerate(range(simulations)):
        asset = Asset(data=data)
        asset._run(61)
        results.append(asset.asset_value(60))
    print("\nComplete.")
        
    result_df = pd.DataFrame(data={"asset_value":results})
    sns.kdeplot(result_df["asset_value"])

