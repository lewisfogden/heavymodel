from heavymodel import Model

class TermAssurance(Model):
    def net_cf(self, t):
        return self.premiums(t) - self.claims(t) - self.expenses(t)

    def premium_pp(self, t):
        """monthly premium"""
        return self.annual_premium / 12

    def claim_pp(self, t):
        if t == 0:
            return self.sum_assured
        elif t > self.term_y * 12:
            return 0
        elif self.shape == "level":
            return self.sum_assured
        elif self.shape == "decreasing":
            r = (1+0.07)**(1/12)-1
            S = self.sum_assured
            T = self.term_y * 12
            outstanding = S * ((1+r)**T - (1+r)**t)/((1+r)**T - 1)
            return outstanding
        else:
            raise ValueError("Parameter 'shape' must be 'level' or 'decreasing'")

    def inflation_factor(self, t):
        """annual"""
        return (1 + self.cost_inflation_pa)**(t//12)

    def premiums(self, t):
        return self.premium_pp(t) * self.num_pols_if(t)

    def duration(self, t):
        """duration in force in years"""
        return t//12

    def claims(self, t):
        return self.claim_pp(t) * self.num_deaths(t)

    def expenses(self, t):
       return self.num_pols_if(t) * self.expense_pp/12 * self.inflation_factor(t)

    def num_pols_if(self, t):
        """number of policies in force"""
        if t==0:
            return self.init_pols_if
        elif t > self.term_y * 12:
            return 0
        else:
            return self.num_pols_if(t-1) - self.num_exits(t-1) - self.num_deaths(t-1)


    def num_exits(self, t):
        """exits occurring at time t"""
        return self.num_pols_if(t) * (1-(1-self.lapse_rate_pa)**(1/12))


    def num_deaths(self, t):
        """deaths occurring at time t"""
        return self.num_pols_if(t) * self.q_x_12(t)

    def age(self, t):
        return self.age_at_entry + t//12


    def q_x_12(self, t):
        return 1-(1-self.q_x_rated(t))**(1/12)

    def qx_mn(self, t):
        return self.mort_qx_mn[self.age(t), self.duration(t)]

    def qx_fn(self, t):
        return self.mort_qx_fn[self.age(t), self.duration(t)]

    def qx_ms(self, t):
        return self.mort_qx_ms[self.age(t), self.duration(t)]

    def qx_fs(self, t):
        return self.mort_qx_fs[self.age(t), self.duration(t)]

    def q_x(self, t):
        # TODO: if basis.gender_neutral == 1 then do this, else use either m or f.
        if self.gender_neutral == 1:
            mn_prop = self.qx_mn_prop
            ms_prop = self.qx_ms_prop
        elif self.gender_neutral == 0:
            mn_prop = 1 * (self.sex=="M")
            ms_prop = 1 * (self.sex=="M")
        if self.smoker_status == "N":
            return mn_prop * self.qx_mn(t) + (1-mn_prop) * self.qx_fn(t)
        elif self.smoker_status == "S":
            return ms_prop * self.qx_ms(t) + (1-ms_prop) * self.qx_fs(t)

    def q_x_rated(self, t):
        return max(0, min(1 , self.q_x(t) * (1 + self.extra_mortality) ) )

    def commission(self, t):
        return 0
