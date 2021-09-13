# ctsm_scripts

Helper scripts for creating and submitting CTSM/FATES jobs on Cheyenne and Izumi.

## config_parse

parses a config file (e.g. *ctsm.config*), when sourced makes parameters available as bash variables. New parameters can be added as needed - see comments in file.

#### Usage:

    source config_parse ctsm.config
    echo ${MACH}
    
## create_build

creates, sets up, and builds a case based on an input config file - makes use of the **config_parse** script

#### Usage:

    ./create_build ctsm.config
    

## create_build_singlpt

creates, sets up, and builds a single-point case based on an input config file - makes use of the **config_parse** script

#### Usage:

    ./create_build_singlept ctsm.config
    
 
## modify_param.py

creates and modifies a default FATES parameter file based on an input csv file. The csv file should have the first column be the FATES PFT index, the second column be the name of the PFT, and then the following columns should have the FATES parameter as the header (matching the FATES parameter file), with values in the cells below it:

| pft_index       | pft_name        | fates_woody     | fates_alloc_storage_cushion |
| --------------- | --------------- | --------------- |  -------------------------- |
| 2 | pice_mari | 1 | 1.2 | 
| 2 | pinu_bank | 1| 1.2 |
| 6 | popu_trem | 1| 1.2 |

#### Usage:

    python3 modify_param.py
