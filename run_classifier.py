#!/usr/bin/python3.8

import argparse
import os
import sys
import pandas as pd
from os import listdir
from os.path import isfile, join

db_type_dict = {
    "refseq": "/root/kraken2/minikraken2_v1_8GB",
    "silva": "/root/kraken2/16S_SILVA138_k2db",
    "greengenes": "/root/kraken2/16S_Greengenes_k2db",
    "rdp": "/root/kraken2/16S_RDP_k2db",
}

compression_type_dict = {
    "gzip": "--gzip-compressed",
    "bzip2": "--bzip2-compressed",
    "none": "",  
}

library_type_dict = {
    "paired": "--paired",
    "single-end": "",
    "fasta": "",
}


def read_library(path_to_library):
    
    reads_dict = {}
    
    with open(path_to_library) as f:
        for line in f:
            if line.startswith("#"):
                continue
            prefix = line.strip().split()[0]
            reads = line.strip().split()[1:3]
            reads_dict[prefix] = reads
    
    return reads_dict
    
def run_classifier(reads_library, library_type, compression_type, database_type, output_folder):
    
    for prefix, reads in reads_library.items():
        
        reads_input = " ".join(reads)    
        
        cmd_1 = f"kraken2 --report {output_folder}/{prefix}.report --output {output_folder}/{prefix}.output "
        cmd_2 = f"--db {db_type_dict[database_type]}  {compression_type_dict[compression_type]} "
        cmd_3 = f"{library_type_dict[library_type]} {reads_input}"
        
        full_cmd = cmd_1 + cmd_2 + cmd_3
        
        print(full_cmd)
        
        os.system(full_cmd)
        
def build_taxa(output_folder, tax_hierarchy):

    onlyfiles = [f for f in listdir(output_folder) if isfile(join(output_folder, f))]
    reports_dict = {}
    for filename in onlyfiles:
        if filename.endswith(".report"):
            file_dict = {}
            filepath = str(output_folder + filename)
            for tax_line in open(filepath, "r"):
                tax_values = tax_line.strip().split('\t')
                taxonomy = tax_values[5].lstrip(" ")
                percentage = tax_values[0]
                rank = tax_values[3]
                if rank == tax_hierarchy:
                    file_dict[taxonomy] = percentage
            reports_dict[filename.split('.')[0]] = file_dict
    
    return reports_dict

def build_df(taxa_dict, database_type, tax_hierarchy, output_folder):
    df = pd.DataFrame.from_dict(taxa_dict).fillna(0)
    df = df.rename_axis('Taxa')
    output_name = str(output_folder + database_type)
    df.to_csv(f"{output_name}_{tax_hierarchy}_tax.csv", index=True, header=True)


def main():
    parser = argparse.ArgumentParser(
        description="Script that runs kraken2 classifier"
    )
    parser.add_argument("-l", 
                        "--path_to_library", 
                        required=True,
                        help="path to the file that contains library reads"
    )
    parser.add_argument("-t",
                        "--library_type",
                        required=True,
                        help="library type: paired, single-end, fasta"
    )
    parser.add_argument("-c",
                        "--compression_type",
                        required=True,
                        help="compression type: gzip, bzip, none"
    )
    parser.add_argument("-d",
                        "--database_type",
                        required=True,
                        help="database type: refseq, silva, greengenes, rdp"
    )
    parser.add_argument("-o",
                        "--output_folder",
                        required=True,
                        help="path to output folder"
    )
    parser.add_argument("-th",
                        "--tax_hierarchy",
                        required=True,
                        help="tax_hierarchy: P, C, O, F, G, S, S1"
    )

    
    
    args = parser.parse_args()
    path_to_library = args.path_to_library
    library_type = args.library_type
    compression_type = args.compression_type
    database_type = args.database_type
    tax_hierarchy = args.tax_hierarchy
    output_folder = args.output_folder
    
    
    # function calling
    reads_library = read_library(path_to_library)
    run_classifier(reads_library, library_type, compression_type, database_type, output_folder)
    taxa_dict = build_taxa(output_folder, tax_hierarchy)
    build_df(taxa_dict, database_type, tax_hierarchy, output_folder)
    

if __name__ == '__main__':
    main()
    
