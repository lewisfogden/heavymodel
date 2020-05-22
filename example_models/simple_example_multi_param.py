# -*- coding: utf-8 -*-

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

    def value_by_duration(self, t, dur):
        #print(f"calling value_by_duration: t:{t} , dur: {dur}")
        if t == 0 or dur == 0:
            return 100
        else:
            return self.value_by_duration(t-1, dur-1) * 1.04

    def value(self, t):
        #print(f"calling value: {t}")
        return sum(self.value_by_duration(t, dur) for dur in range(t))

demo = DemographicModel()

demo._run(2000)

#df = pd.DataFrame({"num_lapses":demo.num_lapses.values, "pol_value":demo.value.values})
#sns.lineplot(data=df)
