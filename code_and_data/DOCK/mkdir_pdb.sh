#!/bin/bash

# Specify the directory containing the files
dir="/home/zhangtm/Insect/Fun_evolution_analysis/All_OR_DOCK/1-USalign/All_9513_align_pdb"

# Iterate over all *_alignOR5.pdb files in the specified directory
for file in ${dir}/*_alignOR5.pdb; do
    # Extract the file name from the path
    #只要文件名没有空格，$file就可以不用加引号
    filename=$(basename $file)

    # Extract the prefix
    pdbname="${filename%_alignOR5.pdb}"
    # Create a directory with the prefix name
    mkdir -p "${pdbname}"

    # Copy the *_alignOR5.pdb file to the new directory and rename it to rec.pdb
    cp ${file} "${pdbname}/rec.pdb"
    
    # Copy the xtal-lig.pdb file to the new directory
    cp "xtal-lig.pdb" "${pdbname}/"
done