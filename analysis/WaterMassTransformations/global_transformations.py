import doralite
import gfdl_utils.core as gu
from CM4Xutils import *

import xbudget
import regionate
import xwmb
import warnings

def save_wmb(grid, model):

    budgets_dict = xbudget.load_preset_budget(model="MOM6_3Donly")
    xbudget.collect_budgets(grid, budgets_dict)
    
    lam = "sigma2"
    with warnings.catch_warnings():
        warnings.simplefilter(action='ignore', category=FutureWarning)

        print("Computing WMT integrals")
        # Spatially-integrated water mass budget terms
        kwargs = {"greater_than":True, "default_bins":True}
        wmb = xwmb.WaterMassBudget(
            grid,
            budgets_dict
        )
        wmb.mass_budget(lam, integrate=True, along_section=False, **kwargs)
        wmb.wmt.to_zarr(f"../../data/wmb_{model}_global_2340-2349.zarr", mode="w")

grid_dict = {}
models = exp_dict.keys()
for model in models:
    ds = concat_scenarios([
        load_wmt_ds(model, interval="2340", dmget=True).isel(time_bounds=slice(None, -1)),
        load_wmt_ds(model, interval="2345", dmget=True)
    ])

    grid_dict[model] = make_wmt_grid(ds)


for model, grid in grid_dict.items():
    save_wmb(grid, model)
