"""
This script parses ./raw/labels.txt and generates a npy file with the parsed data.
"""
import numpy as np
import os
import argparse

PATH = './raw/labels.txt'
OUTPUT_PATH = './processed/labels.npy'

def parse(input_path, output_path):
    with open(input_path, 'r') as f:
        lines = f.readlines()
    labels = [line.strip() for line in lines]

    np.save(output_path, labels)
    print(f"[SAVED] Parsed {len(labels)} labels and saved to {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse labels.txt and save as .npy file")
    parser.add_argument('--input', type=str, default=PATH, help='Path to the input file')
    parser.add_argument('--output', type=str, default=OUTPUT_PATH, help='Path to the output file')
    args = parser.parse_args()

    if not os.path.exists(args.input):
        raise FileNotFoundError(f"{args.input} not found. Please ensure the file exists.")

    last_created_time = os.path.getctime(args.output)
    last_modified_time = os.path.getmtime(args.input)
    if last_modified_time < last_created_time:
        print(f"[INFO] {args.output} is up to date.")
    else:
        print(f"[INFO] {args.output} is outdated.")
        parse(args.input, args.output)