"""
Modifies FATES parameter file based on an input csv file.
"""
import os
import pandas as pd


def change_value(src_dir, out_file, var, val, pft):
    """
    Changes the values of a FATES parameter file for a specified parameter
    """

    script = os.path.join(src_dir, "tools/modify_fates_paramfile.py")
    files = f" --fin {out_file} --fout {out_file} --O "
    command = f"{script} {files} --PFT {pft} --var {var} --val {val}"
    os.system(command)


def modify_fates_params(default_file, out_dir, tag, src_dir, param_file):
    """
    Modifies a FATES parameter file based on an input data frame
    """
    # File name of final nc file
    out_file = os.path.join(out_dir, f"param_file_{tag}.nc")

    command = f"cp {default_file} {out_file}"
    os.system(command)

    # parmaeters to modify
    params = param_file.columns[2:].values

    # Modify all other params
    for parm in params:
        vals = param_file[parm].values
        for vnum, val in enumerate(vals):
            pft = param_file.pft_index.values[vnum]
            change_value(src_dir=src_dir, out_file=out_file, var=str(parm), val=str(val),
                         pft=str(pft))

if __name__ == "__main__":
    CODE_DIR = "/Users/afoster/Documents/ctsm/ctsm_fates/src/fates"
    OUTPUT_DIR = "/Users/afoster/Documents/ctsm/fates/NEON/parameter_files"

    SITE = "BONA"

    file_tag = f"{SITE}_noagb"
    infile = f"/Users/afoster/Documents/ctsm/fates/NEON/parameter_files/fates_{SITE.lower()}_params_noagb.csv"
    default_file = f"/Users/afoster/Documents/ctsm/fates/NEON/parameter_files/param_file_{SITE}_oob.nc"

    # Generate the new parameter file
    param_dat = pd.read_csv(infile)
    modify_fates_params(default_file=default_file, out_dir=OUTPUT_DIR, tag=file_tag,
                        src_dir=CODE_DIR, param_file=param_dat)
