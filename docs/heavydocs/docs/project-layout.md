## Typical Project layout

`heavymodel` places no constraints on how you set up a model, a typical structure is outlined below:

    run_model.py             # The run file.
    heavymodel/
        model.py             # Key Code for model
		basis.py
		data.py
		...                  # Other files
		
	models/                  # Store user models here
	    protection_model.py
		protection_pricing_basis.yaml
		tables/
			uk_zero_spot.csv # Yield Curve
			qx_TFNL08.csv    # Mortality Curve

