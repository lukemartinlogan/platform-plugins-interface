In this section we go over how to install and deploy OrangeFS.
NOTE: if running in Ares, OrangeFS is already installed, so skip
to section 5.3.

# Install Various Dependencies

```bash
sudo apt update
sudo apt install -y fuse
sudo apt install gcc flex bison libssl-dev libdb-dev linux-headers-$(uname -r) perl make libldap2-dev libattr1-dev
```

For fuse
```bash
sudo apt -y install fuse
spack install libfuse@2.9
```

NOTE: This package expects a working, passwordless SSH setup if you are using multiple nodes. On systems like Chameleon Cloud, you
must distribute the keys and set this up yourself before using jarvis. On single-node systems, SSH is not required.

# Install OrangeFS (Linux)

OrangeFS is located [on this website](http://www.orangefs.org/?gclid=CjwKCAjwgqejBhBAEiwAuWHioDo2uu8wel6WhiFqoBDgXMiVXc7nrykeE3sf3mIfDFVEt0_7SwRN8RoCdRYQAvD_BwE)
The official OrangeFS github is [here](https://github.com/waltligon/orangefs/releases/tag/v.2.9.8).

```bash
scspkg create orangefs
cd `scspkg pkg src orangefs`
wget https://github.com/waltligon/orangefs/releases/download/v.2.10.0/orangefs-2.10.0.tar.gz
tar -xvzf orangefs-2.10.0.tar.gz
cd orangefs
./prepare
./configure --prefix=`scspkg pkg root orangefs` --enable-shared --enable-fuse
make -j8
make install
scspkg env prepend orangefs ORANGEFS_PATH `scspkg pkg root orangefs`
```

# Using MPICH with OrangeFS

MPICH requires a special build when using OrangeFS. Apparantly it's for
performance, but it's a pain to have to go through the extra step.

```bash
scspkg create orangefs-mpich
cd `scspkg pkg src orangefs-mpich`
wget http://www.mpich.org/static/downloads/3.2/mpich-3.2.tar.gz --no-check-certificate
tar -xzf mpich-3.2.tar.gz
cd mpich-3.2
./configure --prefix=`scspkg pkg root orangefs-mpich` --enable-fast=O3 --enable-romio --enable-shared --with-pvfs2=`scspkg pkg root orangefs` --with-file-system=pvfs2
make -j8
make install
```

# Creating a pipeline

## Main Parmaeters
There are a few main parameters:
* ``ofs_data_dir``: The place where orangefs should store data or metadata. 
This needs to be a directory private to each node. For example, like /tmp or a burst buffer.
* ``mount``: Where the client should be mounted. This is where users will typically place data.
* ``ofs_mode``: The deployment method to use. Either fuse, kern, or ares.
* ``name``: The semantic name of the OrangeFS deployment. Typically just leave as default unless 
you have multiple deployments

## Performance Parameters
* ``stripe_size``: Size in bytes for stripes. Default 65536 (i.e., 64KB). 
* ``protocol``: Either tcp or ib. Only tcp has been tested.

## The Hostfile
OrangeFS can be picky about the hostfile. We recommend using only IP addresses
in your jarvis hostfile at this time when using OrangeFS.

An example hostfile for a single-node deployment is below:
```bash
echo '127.0.0.1' > ~/hostfile.txt
jarvis hostfile set ~/hostfile.txt
```

## libfuse
```bash
module load orangefs
jarvis pipeline create orangefs
jarvis pipeline env build +ORANGEFS_PATH
jarvis pipeline append orangefs \
mount=${HOME}/orangefs_client \
ofs_data_dir=${HOME}/ofs_data \
ofs_mode=fuse
```

## For kernel module
```bash
module load orangefs
jarvis pipeline create orangefs
jarvis pipeline env build +ORANGEFS_PATH
jarvis pipeline append orangefs \
mount=${HOME}/orangefs_client \
ofs_data_dir=/mnt/nvme/$USER/ofs_data \
ofs_mode=kern
```

## Ares Machine at IIT
```bash
module load orangefs
jarvis pipeline create orangefs
jarvis pipeline env build +ORANGEFS_PATH
jarvis pipeline append orangefs \
mount=${HOME}/orangefs_client \
ofs_data_dir=/mnt/nvme/$USER/ofs_data \
ofs_mode=ares
```
