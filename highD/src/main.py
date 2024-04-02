# import sys
# sys.path.append("./parse")

import argparse
import os

from parse import Parse
from hello import Run

def create_args():
    path = os.path.abspath(__file__)
    dir_path = os.path.dirname(path)
    parser = argparse.ArgumentParser(description="ParameterOptimizer")
    parser.add_argument('--mode', default="parse", 
                        type=str,
                        help='run mode :\n 1.parse[default]\n 2.run')
    # --- Input paths ---
    parser.add_argument('--input_path', default=dir_path+"/../data/01_tracks.csv", 
                        type=str,
                        help='CSV file of the tracks')
    parser.add_argument('--input_static_path', default=dir_path+"/../data/01_tracksMeta.csv",
                        type=str,
                        help='Static meta data file for each track')
    parser.add_argument('--input_meta_path', default=dir_path+"/../data/01_recordingMeta.csv",
                        type=str,
                        help='Static meta data file for the whole video')
    # --- Output path ---
    parser.add_argument('--output_path', default=dir_path+"/../hello", 
                        type=str,
                        help='output path')
    

    parsed_arguments = vars(parser.parse_args())
    return parsed_arguments


if __name__=="__main__":
    created_arguments = create_args()
    mode = created_arguments["mode"]
    if mode == "parse":
        Parse(created_arguments)
    elif mode == "run":
        Run()
        