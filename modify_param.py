from datetime import date
import os
import pandas as pd

def modify_fates_params(file_work, tag, src_dir, param_file):
    
    # File name of final nc file
    today = str(date.today())
    mod_fname = file_work + '/param_file_' + tag + '.nc'

    # Create a string of the pfts we want
    pfts = param_file.pft_index.values
    pft_list = ''
    for pft in pfts:
        pft_list = pft_list + str(pft) + ','

    # We don't want final comma
    pft_list = pft_list[:len(pft_list)-1]

    # Get default parameters for desired pfts
    nc_generate(file_work, tag, src_dir, pft_list, mod_fname)

    # Change pft names
    rename_pfts(src_dir, mod_fname, param_file)

    # Variables to modify
    vars = param_file.columns[2:].values

    # Modify all other params
    for i in range(len(vars)):
        vals = param_file[vars[i]].values
        for j in range(len(vals)):
            change_value(src_dir, mod_fname, str(vars[i]), str(vals[j]), str(j + 1))


    command = src_dir + '/tools/modify_fates_paramfile.py --fin ' + mod_fname + ' --fout ' + mod_fname + ' --O --var fates_mort_disturb_frac --val 0.5'
    os.system(command)

    command = 'rm ' + file_work + '/param_file_' + tag + '_temp0.nc'
    os.system(command)

def change_value(src_dir, mod_fname, var, val, pft):

    script = src_dir + '/tools/modify_fates_paramfile.py'
    files = ' --fin ' + mod_fname + ' --fout ' + mod_fname + ' --O '

    command = script + files + ' --PFT ' + pft + ' --var ' + var + ' --val ' + val

    os.system(command)


def nc_generate(file_work, tag, src_dir, pft_list, mod_fname):


    init_file = file_work + '/param_file_' + tag + '_temp0.nc'
    default_file = src_dir + '/parameter_files/fates_params_default.cdl'

    # generate netcdf binary from the cdl file
    command = 'ncgen -o ' + init_file + ' ' + default_file
    os.system(command)
 
    # pull out pfts of interest (needle leaf evergreen: 2; broadleaf decid tree: 6)
    command = src_dir + '/tools/FatesPFTIndexSwapper.py --fin ' + init_file + ' --fout ' + mod_fname + \
              " --pft-indices " + pft_list
    os.system(command)
    
def rename_pfts(src_dir, mod_fname, param_file):

    pft_names = param_file.pft_name.values

    for i in range(len(pft_names)):
        command = src_dir + '/tools/modify_fates_paramfile.py --fin ' + mod_fname + ' --fout ' + mod_fname + \
            ' --O --var fates_pftname --val ' + str(pft_names[i]) + ' --PFT ' + str(i + 1)
        
        os.system(command)


if __name__ == "__main__":
    src_dir = '/project/tss/afoster/ctsm_fates/src/fates'
    file_work = '/project/tss/afoster/FATES_params'
    tag = 'canada'
    infile = '/project/tss/afoster/FATES_params/fates_yukon_parameters.csv'
    
    # Generate the new parameter file
    param_file = pd.read_csv(infile)
    modify_fates_params(file_work, tag, src_dir, param_file)



