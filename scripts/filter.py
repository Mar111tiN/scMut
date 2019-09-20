import os
import subprocess
################### INIT (arguments and data)
w = snakemake.wildcards
config = snakemake.config
filter_name = w.filter
filter_config = config['filter'][filter_name]
input_file = snakemake.input[0]
output_file = snakemake.output[0]


def get_filter(f):
    '''
    takes the filter dictionary and returns full path to the filter script using filter['name']
    '''

    return os.path.join(config['snakedir'], config['paths']['scripts'], 'filters', f['path'])

# get and run the respective filter as a shell script:
print(f"Running filter {filter_name}")
filter_script = get_filter(filter_config)

# prepare CLI filter call:
# convert params from config into space-separated list
params_list = [param for plist in [[f"-{param}", f"{val}"] for param, val in filter_config['params'].items()] for param in plist]
filter_cmd = [filter_script, *params_list, input_file, output_file]

print(f" ".join(filter_cmd))
success = subprocess.call(filter_cmd)