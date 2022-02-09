# automatic_kk2_classifier
Dockerfile with kraken2 and a script for automatization

## Installation

### Clone repositorie

`git clone git@github.com:FelipeMelis/automatic_kk2_classifier.git`

### Download test from Google drive to root directory

https://drive.google.com/drive/folders/1zb2SZ8-lsBAuc-xGdSo-4M2066W3Zy2D
###Build docker image

`docker build -t bacterial_classifier .`
### Run docker image and mount current dir

`docker run -it -v $PWD:/DATA --rm bacterial_classifier`

## Updating databases

### Go to kraken2 index webpage

1. Index webpage https://benlangmead.github.io/aws-indexes/k2
2. Download selected database to kraken2 root folder
3. Extract the content to a folder with a **name related to the DB**
4. Modify the `config.py` and add the name of the DB and path

### Example

1. Download Viral database to `/root/kraken2/` and extract to `k2_viral` 
<img width="782" alt="Screen Shot 2022-02-09 at 09 50 17" src="https://user-images.githubusercontent.com/15635619/153204503-597251b7-daee-4b70-bb60-0a5a6d336e23.png">


2.- Modify `config.py` and add `"viral": "/root/kraken2/k2_viral"` to the python dict

    DATABASE_TYPE = {
        "refseq": "/root/kraken2/minikraken2_v1_8GB",
        "silva": "/root/kraken2/16S_SILVA138_k2db",
        "greengenes": "/root/kraken2/16S_Greengenes_k2db",
        "rdp": "/root/kraken2/16S_RDP_k2db",
        "viral": "/root/kraken2/k2_viral" #New database
    }

3.- The database will appear at option `-d` and will be ready to use with that name
```
usage: run_classifier.py [-h] -l PATH_TO_LIBRARY -t LIBRARY_TYPE -c COMPRESSION_TYPE -d DATABASE_TYPE -o OUTPUT_FOLDER -th TAX_HIERARCHY -cpus CPU_NUMBER

Script that runs kraken2 classifier

optional arguments:
  -h, --help            show this help message and exit
  -l PATH_TO_LIBRARY, --path_to_library PATH_TO_LIBRARY
                        path to the file that contains library reads
  -t LIBRARY_TYPE, --library_type LIBRARY_TYPE
                        library type: ['paired', 'single-end', 'fasta']
  -c COMPRESSION_TYPE, --compression_type COMPRESSION_TYPE
                        compression type: ['gzip', 'bzip2', 'none']
  -d DATABASE_TYPE, --database_type DATABASE_TYPE
                        DB type: ['refseq', 'silva', 'greengenes', 'rdp', 'viral']
  -o OUTPUT_FOLDER, --output_folder OUTPUT_FOLDER
                        path to output folder
  -th TAX_HIERARCHY, --tax_hierarchy TAX_HIERARCHY
                        tax_hierarchy: P, C, O, F, G, S, S1
  -cpus CPU_NUMBER, --cpu_number CPU_NUMBER
                        Number of cpus to be used
