from heavymodel import Model

class TermAssurance(Model):
    def net_cf(m, t):
        return m.premiums(t) - m.claims(t) - m.expenses(t)
    
    def premium_pp(m, t):
        """monthly premium"""
        return m.annual_premium / 12
    
    def claim_pp(m, t):
        if t == 0:
            return m.sum_assured
        elif t > m.term_y * 12:
            return 0
        elif m.shape == "level":
            return m.sum_assured
        elif m.shape == "decreasing":
            r = (1+0.07)**(1/12)-1
            S = m.sum_assured
            T = m.term_y * 12
            outstanding = S * ((1+r)**T - (1+r)**t)/((1+r)**T - 1)
            return outstanding
        else:
            raise ValueError("Parameter 'shape' must be 'level' or 'decreasing'")
    
    def inflation_factor(m, t):
        """annual"""
        return (1 + m.cost_inflation_pa)**(t//12)
      
    def premiums(m, t):
        return m.premium_pp(t) * m.num_pols_if(t)
    
    def duration(m, t):
        """duration in force in years"""
        return t//12
    
    def claims(m, t):
        return m.claim_pp(t) * m.num_deaths(t)
      
    def expenses(m, t):
       return m.num_pols_if(t) * m.expense_pp/12 * m.inflation_factor(t)
      
    def num_pols_if(m, t):
        """number of policies in force"""
        if t==0:
            return m.init_pols_if
        elif t > m.term_y * 12:
            return 0
        else:
            return m.num_pols_if(t-1) - m.num_exits(t-1) - m.num_deaths(t-1)
    
      
    def num_exits(m, t):
        """exits occurring at time t"""
        return m.num_pols_if(t) * (1-(1-m.lapse_rate_pa)**(1/12))
      
      
    def num_deaths(m, t):
        """deaths occurring at time t"""
        return m.num_pols_if(t) * m.q_x_12(t)
    
    def age(m, t):
        return m.age_at_entry + t//12
    
    
    def q_x_12(m, t):
        return 1-(1-m.q_x_rated(t))**(1/12)
    
    def qx_mn(m, t):
        return m.mort_qx_mn[m.age(t), m.duration(t)]
    
    def qx_fn(m, t):
        return m.mort_qx_fn[m.age(t), m.duration(t)]
    
    def qx_ms(m, t):
        return m.mort_qx_ms[m.age(t), m.duration(t)]
    
    def qx_fs(m, t):
        return m.mort_qx_fs[m.age(t), m.duration(t)]
    
    def q_x(m, t):
        # TODO: if basis.gender_neutral == 1 then do this, else use either m or f.
        if m.gender_neutral == 1:
            mn_prop = m.qx_mn_prop
            ms_prop = m.qx_ms_prop
        elif m.gender_neutral == 0:
            mn_prop = 1 * (m.sex=="M")
            ms_prop = 1 * (m.sex=="M")
        if m.smoker_status == "N":
            return mn_prop * m.qx_mn(t) + (1-mn_prop) * m.qx_fn(t)
        elif m.smoker_status == "S":
            return ms_prop * m.qx_ms(t) + (1-ms_prop) * m.qx_fs(t)
            
    def q_x_rated(m, t):
        return max(0, min(1 , m.q_x(t) * (1 + m.extra_mortality) ) )
        
    def commission(m, t):
        return 0
