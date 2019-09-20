import os
import re
import yaml
from collections import namedtuple
import argparse


# ############ SETUP ##############################
configfile: "configs/config.yaml"
# configfile: "configs/config.json"
workdir: config['workdir']


# ############ INCLUDES ##############################
# include helper functions
include: "includes/io.snk"
include: "includes/utils.snk"

include: "includes/coverage.snk"
include: "includes/mut_detect.snk"


# globals
chroms = [num + 1 for num in range(22)] # x and y have no mapping
wildcard_constraints:
    # eg sample cannot contain _ or / to prevent ambiguous wildcards
    sample = "[^_/]+"


rule all:
    input:
        expand("covcsv/{sample}_{cov_level}_{orient}.csv", sample=config['samples'], cov_level=['Mol', 'UMI'], orient=['5', '3'])


# print out of the installed tools
onstart:
    print("    scRNA 10x COVERAGE ANALYSIS STARTING.......")
    ##########################
    # write config to the results directory
    path_to_config = os.path.join(config['workdir'], "config.yaml")
    with open(path_to_config, 'w+') as stream:
        yaml.dump(config, stream, default_flow_style=False)

onsuccess:
    # shell("export PATH=$ORG_PATH; unset ORG_PATH")
    print("Workflow finished - everything ran smoothly")