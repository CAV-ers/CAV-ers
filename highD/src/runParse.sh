#!/bin/bash

index=$1
if [ -z $index ];
then
    index="1"
fi
index=$(printf "%02d" $index)

python main.py \
    --input_path         ./../data/${index}_tracks.csv \
    --input_static_path  ./../data/${index}_tracksMeta.csv \
    --input_meta_path    ./../data/${index}_recordingMeta.csv \
    --output_path        ./../hello