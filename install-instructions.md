# Install Guide:


## Clone the repo:

git clone https://github.com/cheeberger/Economist2Epub.git](https://github.com/calebbrgr/Economist2Epub.git

cd ./Economist2Epub

python3 -r requirements.txt


## Install Golang:

wget https://dl.google.com/go/go1.18.3.linux-amd64.tar.gz 

sudo tar -xvf go1.18.3.linux-amd64.tar.gz

sudo mv go /usr/local

*Make sure your go path is set correctly; adding the following to .bashrc/.zshrc:*

export GOROOT=/usr/local/go

export GOPATH=$HOME/go

export PATH=$GOPATH/bin:$GOROOT/bin:$PATH


## Install Papeer:

go install github.com/lapwat/papeer@latest


## Install Pandoc:

wget https://hackage.haskell.org/package/pandoc-1.17.0.3/pandoc-1.17.0.3.tar.gz

tar xvzf pandoc-1.17.0.3.tar.gz

## Run:

python3 main.py

The epub file can now be found in ./ebooks for your use. Personally I load the file to my ereader with [calibre](https://github.com/kovidgoyal/calibre).
