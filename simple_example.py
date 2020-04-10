# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 21:32:06 2020

@author: user
"""
import pandas as pd
import seaborn as sns
sns.set()

from heavymodel import Model

class DemographicModel(Model):
	def num_policies(self, t):
		if t == 0:
			return 1
		else:
			return self.num_policies(t-1) - self.num_lapses(t-1)
	
	def num_lapses(self, t):
		return 0.1 * self.num_policies(t)

demo = DemographicModel()

demo._run(20)

df = pd.DataFrame({"num_lapses":demo.num_lapses.values, "num_policies":demo.num_policies.values})
sns.lineplot(data=df)