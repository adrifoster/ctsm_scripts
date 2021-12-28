"""
Modifies FATES parameter file based on an input csv file.
"""
import os
import pandas as pd


def nc_generate(out_dir, src_dir, pfts, out_file):
    """
    Generates a FATES default parameter file with only the pfts specified
    """
    # name of output file with swapped PFTs
    temp_file = os.path.join(out_dir, "param_file_temp0.nc")

    # name of default input file
    default_file = os.path.join(src_dir, "parameter_files/fates_params_default.cdl")

    # generate netcdf binary from the cdl file
    os.system(f"ncgen -o {temp_file} {default_file}")

    # list of pfts from array
    pft_list = str(pfts).join(",")

    # pull out pfts of interest
    script = os.path.join(src_dir, 'tools/FatesPFTIndexSwapper.py')
    command = f"{script} --fin {temp_file} --fout {out_file} --pft-indices {pft_list} "
    os.system(command)


def rename_pfts(src_dir, file_name, param_file):
    """
    Renames PFTs for a FATES parameter file based on an input file.
    """
    # pull out pft names from input file
    pft_names = param_file.pft_name.values

    # rename the pfts
    script = os.path.join(src_dir, "tools/modify_fates_paramfile.py")
    for num, pft in enumerate(pft_names):
        command = f"{script} --fin {file_name} --fout {file_name} --O --var fates_pftname " \
                  f"--val {pft} --PFT {num + 1}"
        os.system(command)

def change_value(src_dir, out_file, var, val, pft):
    """
    Changes the values of a FATES parameter file for a specified parameter
    """

    script = os.path.join(src_dir, "/tools/modify_fates_paramfile.py")
    files = f" --fin {out_file} --fout {out_file} --0 "
    command = f"{script} {files} --PFT {pft} --var {var} --val {val}"
    os.system(command)

def modify_fates_params(out_dir, tag, src_dir, param_file):
    """
    Modifies a FATES parameter file based on an input data frame
    """
    # File name of final nc file
    out_file = os.path.join(out_dir, f"param_file_{tag}.nc")

    # create a string of the pfts we want
    pfts = param_file.pft_index.values

    # get default parameters for desired pfts
    nc_generate(out_dir, src_dir, pfts, out_file)

    # change pft names
    rename_pfts(src_dir, out_file, param_file)

    # parmaeters to modify
    params = param_file.columns[2:].values

    # Modify all other params
    for parm in enumerate(params):
        vals = param_file[parm].values
        for vnum, val in vals:
            change_value(src_dir, out_file, str(parm), str(val), str(vnum + 1))

    # set disturbance fraction to 0.5
    script = os.path.join(src_dir, "tools/modify_fates_paramfile.py")
    command = f"{script} --fin {out_file} --fout {out_file} --O --var fates_mort_disturb_frac " \
              f"--val 0.5 "
    os.system(command)

    # delete the temporary file
    os.system(f"rm {os.path.join(out_dir, 'param_file_temp0.nc')}")


if __name__ == "__main__":
    CODE_DIR = "/project/tss/afoster/ctsm_fates/src/fates"
    OUTPUT_DIR = "/project/tss/afoster/FATES_params"
    FILE_TAG = "canada"
    INFILE = "/project/tss/afoster/FATES_params/fates_yukon_parameters.csv"

    # Generate the new parameter file
    param_dat = pd.read_csv(INFILE)
    modify_fates_params(OUTPUT_DIR, FILE_TAG, CODE_DIR, param_dat)
