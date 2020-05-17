# -*- coding: utf-8 -*-

from models.protection_model import TermAssurance
from heavymodel import Data, Basis
from heavymodel.pricing import solve_prot_premium, get_bel
#TODO: add Basis.read_yaml as a @classmethod
#TODO: add Basis.read_xml as a @classmethod


if __name__=='__main__':

    pricing_basis = Basis.read_yaml(r"models/protection_pricing_basis.yaml")
    valuation_basis = Basis.read_yaml(r"models/protection_pricing_basis.yaml")

    quote = {
        "sum_assured":1000000,
        "age_at_entry":35,
        "term_y":20,
        "smoker_status":"N",
        "shape":"decreasing",
        "annual_premium":1,
        "init_pols_if":1,
        "extra_mortality":0,
        "sex":"M"
    }
    data = Data(quote)

    monthly_premium = solve_prot_premium(TermAssurance, data, pricing_basis)
    print("Premium: ", monthly_premium)

    bel_data = Data(quote)
    bel_data.annual_premium = monthly_premium * 12
    bel = get_bel(TermAssurance, bel_data, pricing_basis)
    print("BEL (gender neutral):  ", bel)

    valuation_basis.gender_neutral = 0
    bel = get_bel(TermAssurance, bel_data, valuation_basis)
    print("BEL (gender specific): ", bel)

    print(bel)
