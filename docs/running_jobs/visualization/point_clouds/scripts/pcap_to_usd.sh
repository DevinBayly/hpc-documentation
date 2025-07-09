#!/bin/bash
pcap=$1
json=$2
pyscript=$3
mapscript=$4


# ensure that the mapping script contains the correct latest instructions
cp $mapscript /usr/local/lib/python3.10/dist-packages/ouster/cli/plugins/source_mapping.py

starting_dir=$(pwd -P)
folder_path=$(echo $pcap | sed 's/\.[^.]*$//')
fname=$(echo $pcap | sed 's/\.[^.]*$//' | sed 's/.*\///')
# move everything to a folder in /tmp
echo making directory ${name} in tmp
mkdir -p /tmp/${folder_path}
cp $pcap /tmp/${folder_path}
cp $json /tmp/${folder_path}
cp $pyscript /tmp/${folder_path}

cd /tmp/
echo $pcap is a file
echo /tmp/${folder_path}/${fname} is path
cd /tmp/${folder_path}/
ouster-cli source ${fname}.pcap slam save "${fname}.osf"
# makes use of the mapping code from before
ouster-cli source "${fname}.osf" save ${fname}.las

python3 $pyscript ${fname}
rm *pcd

# bring back the usd file 

echo copying back
cp ${fname}.usdc ${starting_dir}
