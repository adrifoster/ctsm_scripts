# ctsm_scripts

Helper scripts for creating and submitting CTSM/FATES jobs on Cheyenne and Izumi.

**config_parse** - parses a config file (e.g. *ctsm.config*), when sourced makes parameters available as bash variables. New parameters can be added as needed - see comments in file.

### Usage:

    source config_parse ctsm.config
    echo ${MACH}
    
**create_build** - creates, sets up, and builds a case based on an input config file - makes use of the **config_parse** script

### Usage:

    ./create_build ctsm.config
