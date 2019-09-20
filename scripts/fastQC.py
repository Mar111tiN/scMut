from os import system as shell

config = snakemake.config
w = snakemake.wildcards
path = f'{w.sample}_{w.type}_{w.readtrim}'
lines = round(config['qc']['samplefactor']) * 4
input = snakemake.input
log = snakemake.log

#   run QC on subsamples only if sample factor > 1
if config['qc']['samplefactor'] < 2:
    shell(f"fastqc {input} -o fastQC/ &>{snakemake.log}")
else:
    print(f"Downsampled for QC with factor: {config['qc']['samplefactor']}")
    shell(f"mawk 'NR % {lines} > 0 && NR % {lines} < 5' {input} > {input}.sub")
    shell(f'fastqc {input}.sub -o fastQC/ &>{log}')
    shell(f'mv fastQC/{path}.fastq.sub_fastqc.zip fastQC/{path}_fastqc.zip')