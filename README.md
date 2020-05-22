# Heavymodel

heavymodel is a class-based library which enables Actuaries (and other modelling professionals) to build actuarial models in Python, using a function-based syntax similar to other actuarial modelling software, combined with the simplicity of writing code in python.

## Installation

Install via pip:

`pip install heavymodel-lewisfogden`

## Simple Model Creation

Import heavymodel, and then subclass your own model from `Model`:

```python
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
```

See https://www.digitalactuary.co.uk/ for further documentation.


