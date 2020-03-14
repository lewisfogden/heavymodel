# pricing.py

from .data import Data
#from opus.basis import load_basis

def solve_prot_premium(model, data=None, basis=None):
    
    model_inst = model(data, basis)
  
    pricing_entries = Data({
            "annual_premium":1,
            "init_pols_if":1,
            "extra_mortality":0
            })
    
    model_inst._update(pricing_entries, warn=False)
    
    proj_len = data.term_y*12+1
    
    def npv(cashflow):
        pv = 0.0
        for t in range(0, proj_len):
            pv += basis.rfr.v[t] * cashflow(t)
        return pv

    # project cashflows
    model_inst._run(proj_len)
            
    # calculate npvs
    npv_claims = npv(model_inst.claims)
    npv_expenses = npv(model_inst.expenses)
    npv_commission = npv(model_inst.commission)
    npv_premiums = npv(model_inst.premiums)
            
    # calculate premium
    
    annual_risk_premium = (npv_claims + npv_expenses + npv_commission) / npv_premiums
    monthly_risk_premium = annual_risk_premium / 12
    commercial_premium = model_inst.k_factor * monthly_risk_premium + model_inst.c_factor
    commercial_premium = round(commercial_premium, 2)
    
    return commercial_premium


def get_bel(model, data=None, basis=None):
    
    model_inst = model(data, basis)
   
    proj_len = data.term_y*12+1
    
    def npv(cashflow):
        pv = 0.0
        for t in range(0, proj_len):
            pv += basis.rfr.v[t] * cashflow(t)
        return pv

    # project cashflows
    model_inst._run(proj_len)
            
    # calculate npvs
    npv_claims = npv(model_inst.claims)
    npv_expenses = npv(model_inst.expenses)
    npv_commission = npv(model_inst.commission)
    npv_premiums = npv(model_inst.premiums)
    bel = npv_claims + npv_expenses + npv_commission - npv_premiums
    return bel

