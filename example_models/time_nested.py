# nested.py
# minimum reproduceable nested model - for benchmarking purposes
# requirements: pip install heavymodel-lewisfogden pyyaml pandas (sorry if I've missed something :D)

from heavymodel import Model

import timeit

class Term(Model):
    def num_pols_if(self, t):
        """number of policies in force at time t0"""
        if t == 0:
            return 1
        else:
            return self.num_pols_if(t-1) - self.num_deaths(t-1)

    def num_deaths(self, t):
        """number of deaths occurring between time t-1 and time t"""
        if t == 0:
            return 0
        else:
            return self.num_pols_if(t-1) * self.q_x(t-1)

    def term_remaining(self, t):
        return self.data["term_m"] - t

    def q_x(self, t):
        return 0.001 # lazy - would usually look up a table
    
    def age(self, t):
        return self.data["start_age"] + t // 12
    
    def net_cashflow(self, t):
        return self.premiums(t) - self.claims(t)

    def premiums(self, t):
        if 0 <= t < self.data["term_m"] - 1:
            return self.num_pols_if(t) * self.data["premium"] / 12
        else:
            return 0
    
    def claims(self, t):
        if 0 <= t < self.data["term_m"]:
            return self.num_deaths(t) * self.data["sum_assured"]
        else:
            return 0

class RealisticTerm(Term):
    def capital_requirement(self, t):
        """capital to hold at time t, this calls a nested model (PrudentTerm) within term"""
        # set up data, at time t we roll on term_m and start_age
        data = {
            "term_m": self.term_remaining(t),
            "premium": self.data["premium"],
            "sum_assured": self.data["sum_assured"],
            "start_age": self.age(t),
            }
        
        # calculate using a prudent basis, the capital required.
        model = PrudentTerm(data={"data":data})
        model._run(proj_len=data["term_m"] + 1)
        capital_requirement = sum(model.net_cashflow(i) for i in range(data["term_m"] + 1)) # lets not worry about discounting
        return capital_requirement * self.num_pols_if(t)  # only have a requirement for in force policies
    
    def capital_change(self, t):
        if t == 0:
            return self.capital_requirement(t)
        else:
            return -(self.capital_requirement(t-1) - self.capital_requirement(t))


    
class PrudentTerm(Term):
    """Prudent projection of the term model - using a margin of 20% higher deaths than the best estimate, everything else equal"""
    # this would usually be specified through a prudent basis and may be stochastic (e.g. Solvency II).
    def q_x(self, t):
        return 0.001 * 1.2


def do_run():
    data =  {"term_m": 120,
            "premium": 1300,
            "sum_assured": 100_000,
            "start_age": 30,
            }
    
    rw_model = RealisticTerm(data={"data":data})
    rw_model._run(proj_len=data["term_m"] + 1)
    result = sum(rw_model.capital_requirement.values.values())    # meaningless, just for testing
    return result

if __name__ == "__main__":
    import sys
    print("Python Version: ", repr(sys.version))
    print("~"*30)
    result = timeit.repeat('do_run()', repeat=10, number=100, globals = globals())
    print("result of: timeit.repeat('do_run()', repeat=10, number=100, globals = globals())")
    print("Min:  ", min(result))
    print("Max:  ", max(result))
    print("Mean: ", sum(result)/len(result))
    print("")

