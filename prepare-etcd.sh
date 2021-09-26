#!/bin/bash

set -e
set -o pipefail

base=`pwd`
version=$1

if [ "$version" = "" ]; then
    echo "./prepare-etcd.sh: requires a specific version"
    exit 1
fi

mkdir -p etcd/$version

# download wheels from github artifacts
pushd etcd/$version
curl -s https://api.github.com/repos/etcd-io/etcd/releases/tags/$version \
    | grep -e "browser_download_url.*zip" \
           -e "browser_download_url.*tar.gz" \
    | cut -d : -f 2,3 | tr -d \" | wget -qi -
popd

# extract zip/tar.gz
pushd etcd/$version
for artifact in $(ls ./*);
do
    echo "Extracting $artifact ..."
    if [[ $artifact == *"tar.gz" ]]; then
        tar zxvf $artifact
    fi
    if [[ $artifact == *"zip" ]]; then
        unzip $artifact
    fi
done
popd
