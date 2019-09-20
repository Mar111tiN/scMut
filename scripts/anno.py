from os import system as shell


annovar = snakemake.config['tools']['annovar']

w = snakemake.wildcards
file_name = f"{w.sample}_{w.tumor_norm}"
input = snakemake.input
output = snakemake.output
params = snakemake.params
anno_format = params.anno_format
log = snakemake.log
expand_info = params.expand_info
merge_anno = params.merge_anno

for varscan_file in input:
    output_file = varscan_file.replace('varscan.', '').replace('varscan/', '')
    # varscan output has to be converted to avinput file format
    # anno_format adjusts alt, ref and start and end positions for indels
    shell(f"{anno_format} < {varscan_file} > {varscan_file}.avinput")
    print(f"Generated {varscan_file}.avinput")
    # get the annotations
    shell(f"{annovar}/table_annovar.pl {varscan_file}.avinput --outfile annovar/{output_file} {params.pars} &>{log}")
    print(f"Generated annovar/{output_file}")
    # sed script to expand the otherInfo block in the merged anno file to tab_delimited columns
    shell(f"{expand_info} annovar/{output_file}*.txt")
# concatenate indels and snps
shell(f"{merge_anno} -indel annovar/{file_name}.indel*.txt -snp annovar/{file_name}.snp*.txt -out {output}")
print(f"Merged indel and snp annotation into {output}")