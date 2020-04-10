# Definitions

This page provides definitions of the core `heavymodel` functionality.

## `Model` methods:

**NOTE:**User methods should not begin with an underscore (`_`), as this is reserved for core functions. Any user method beginning with an underscore will be skipped when running the model (although still run if it is called by another function), and may inadvertently also conflict with core functions.

initialisation (`__init__(*args, **kwargs)`):

 * the default initialiser parses all supplied parameters and adds these to the namespace of the instance.

`_update(data_or_basis_item)`:

 * adds data or basis to the model space, so it can be referenced by attribute

`_clear_cache()`:

* clears all results from an instance of the model

`_run(proj_len)`:

* evaluates each single parameter function in the model from t = 0 to t = proj_len-1

`_dataframe()`:

* if pandas is installed, returns a dataframe of all results.