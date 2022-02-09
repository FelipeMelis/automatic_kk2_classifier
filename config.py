class Config:

    DATABASE_TYPE = {
        "refseq": "/root/kraken2/minikraken2_v1_8GB",
        "silva": "/root/kraken2/16S_SILVA138_k2db",
        "greengenes": "/root/kraken2/16S_Greengenes_k2db",
        "rdp": "/root/kraken2/16S_RDP_k2db",
    }

    COMPRESSION_TYPE = {
        "gzip": "--gzip-compressed",
        "bzip2": "--bzip2-compressed",
        "none": "",
    }

    LIBRARY_TYPE = {
        "paired": "--paired",
        "single-end": "",
        "fasta": "",
    }