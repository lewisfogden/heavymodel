# Asset Modelling

This section considers modelling of some investment assets (e.g. Unit-Linked funds)

There are various ways to model portfolio of assets, we will look at three here:

 * Nested unit models
 * Individual asset functions
 * Two parameter functions

For brevity, all code is not written, but they provide an outline of the approach.

## Nested Model

```python
class Asset(Model):
	def value(self, t):
		if t == 0:
			return self.init_value
		else:
			return self.value(t-1) * (1 + self.inv_growth)

class Portfolio(Model):
	def value(self, t):
		return sum(asset.value(t) for asset in self.assets)
```

With this approach we initialise each `Asset` and pass these to `Portfolio` model.  One of the benefits of this approach is that we can define different types of asset to have different functions, e.g. a `Bond` class could be defined which allows for the probability of default, as long as it implements the `value(t)` method it can be otherwise written as desired.

```python
my_assets = [Asset(init_value=100, inv_growth=0.04),
		  Asset(init_value=200, inv_growth=0.02)]

my_portfolio = Portfolio(assets = my_assets)

print(my_portfolio.value(10))
```


## Individual Asset Functions

This approach may work well if there are only a few asset classes, the downside is that you need to replicate all the code for each asset class, and manually add them together.

```python
class Investment(Model):
    def fund_value_equity(self, t):
		pass # equity code here
	
	def fund_value_bond(self, t):
		pass # bond code here
		
	def value(self, t):
		return self.fund_value_bond(t) + self.fund_value_equity(t)
```

## Two Parameter (array) Functions

This approach uses a two parameter asset_value function, the second parameter is the name of the asset.  This is similar to modelling Income Protection business when recovery rates are likely to be a function of time and duration of sickness.

```python
class TPF_Portfolio(Model):
	def asset_value(self, t, asset_name):
		if t == 0:
			return self.init_asset_value[asset_name]
		else:
			return self.fund_value(self, t-1, asset_name) * (1 + ...)

	def value(self, t):
		return sum(asset_value(t, asset_name) for asset in self.asset_list)
```

For this approach we need to specify initial values, in practice likely through an assumption file.

```python
assets = ["equity", "bond", "property"]
init_values = {"equity": 1000, "bond": 500, "property": 400}

model = TPF_Portfolio(init_asset_value = init_values, asset_list=assets)
```
