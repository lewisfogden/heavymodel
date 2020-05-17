from heavymodel import Model

class Asset(Model):
    def value(self, t):
        if t == 0:
            return self.init_value
        else:
            return self.value(t-1) * (1 + self.inv_growth)

class Portfolio(Model):
    def value(self, t):
        return sum(asset.value(t) for asset in self.assets)

my_assets = [Asset(data={"init_value":100, "inv_growth":0.04}),
             Asset(data={"init_value":200, "inv_growth":0.02}),
             Asset(data={"init_value":150, "inv_growth":0.05})]

# we need to manually initialise each asset
for asset in my_assets:
    asset._cache_funcs()


# now create the portfolio and run
my_portfolio = Portfolio(data = {"assets":my_assets})

my_portfolio._run(120)

print(my_portfolio.value(120))