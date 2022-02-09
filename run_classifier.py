#!/usr/bin/python3.8

import argparse
import os
import pandas as pd
from os import listdir
from os.path import isfile, join
from config import Config


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


def run_classifier(reads_library,
                   library_type,
                   compression_type,
                   database_type,
                   cpu_number,
                   output_folder):
    
    for prefix, reads in reads_library.items():
        
        reads_input = " ".join(reads)    
        
        cmd = (
            f"kraken2 "
            f"--report {output_folder}/{prefix}.report "
            f"--output {output_folder}/{prefix}.output "
            f"--threads {cpu_number} "
            f"--db {Config.DATABASE_TYPE[database_type]} "
            f"{Config.COMPRESSION_TYPE[compression_type]} "
            f"{Config.LIBRARY_TYPE[library_type]} "
            f"{reads_input}"
        )
        
        os.system(cmd)


def build_taxa(output_folder, tax_hierarchy):

    sys_files = [
        f for f in listdir(output_folder) if isfile(join(output_folder, f))
    ]

    reports_dict = {}
    for filename in sys_files:
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
    df.to_csv(f"{output_name}_{tax_hierarchy}_tax.csv",
              index=True,
              header=True)


def main():
    parser = argparse.ArgumentParser(
        description="Script that runs kraken2 classifier")
    parser.add_argument("-l", 
                        "--path_to_library", 
                        required=True,
                        help="path to the file that contains library reads")
    parser.add_argument("-t",
                        "--library_type",
                        required=True,
                        help=f"library type: "
                             f"{list(Config.LIBRARY_TYPE.keys())}")
    parser.add_argument("-c",
                        "--compression_type",
                        required=True,
                        help=f"compression type: "
                             f"{list(Config.COMPRESSION_TYPE.keys())}")
    parser.add_argument("-d",
                        "--database_type",
                        required=True,
                        help=f"DB type: "
                             f"{list(Config.DATABASE_TYPE.keys())}")
    parser.add_argument("-o",
                        "--output_folder",
                        required=True,
                        help="path to output folder")
    parser.add_argument("-th",
                        "--tax_hierarchy",
                        required=True,
                        help="tax_hierarchy: P, C, O, F, G, S, S1")
    parser.add_argument("-cpus",
                        "--cpu_number",
                        required=True,
                        help="Number of cpus to be used")

    args = parser.parse_args()
    path_to_library = args.path_to_library
    library_type = args.library_type
    compression_type = args.compression_type
    database_type = args.database_type
    tax_hierarchy = args.tax_hierarchy
    cpu_number = args.cpu_number
    output_folder = args.output_folder

    # function calling
    reads_library = read_library(path_to_library)
    run_classifier(reads_library,
                   library_type,
                   compression_type,
                   database_type,
                   cpu_number,
                   output_folder)
    taxa_dict = build_taxa(output_folder, tax_hierarchy)
    build_df(taxa_dict, database_type, tax_hierarchy, output_folder)
    

if __name__ == '__main__':
    main()
    
