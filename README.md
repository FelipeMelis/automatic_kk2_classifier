# automatic_kk2_classifier
Dockerfile with kraken2 and a script for automatization

**Clone repositorie**

`git clone git@github.com:FelipeMelis/automatic_kk2_classifier.git`

**Download test from Google drive to root directory**

https://drive.google.com/drive/folders/1zb2SZ8-lsBAuc-xGdSo-4M2066W3Zy2D

**Build docker image**

`docker build -t bacterial_classifier .`

**Run docker image and mount current dir**

`docker run -it -v $PWD:/DATA --rm bacterial_classifier`
