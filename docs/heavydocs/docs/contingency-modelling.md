# Life Modelling with Python / Actuarial
## Lewis Fogden (lewis@fogden.org / LinkedIn)

### Introduction

This guide provides an overview of an approach to modelling life contingencies using Python.

 - Overall structure
 - Assumptions & Tables
 - Data
 - Model definition - Projection
 - Discounting / valuing
 - Using OOP to minimise code base


# model points

for mp in Model_Points(filename="filename.csv", infer_type=True):
    policy_number = mp["POL_NO"]
    sum_assured = mp["SUM_ASSURED[1:1]"]
    age1_next_birthday = mp["AGE1"]
    
