#!/usr/bin/env python

import argparse
import os
import shutil

parser = argparse.ArgumentParser(description='Move files to directories based on domain matching.')
parser.add_argument('downloads_dir', metavar='DOWNLOADS_DIR', type=str,
                    help='the path to the Downloads folder')
parser.add_argument('--rules', metavar='RULES_FILE', type=str, default=None,
                    help='the path to a file containing rules for domain matching')

args = parser.parse_args()

# Set the path to the Downloads folder
downloads_dir = os.path.expanduser(args.downloads_dir)

# Define rules for moving files to directories based on domain matching
rules = {}
if args.rules:
    with open(args.rules, 'r') as f:
        for line in f:
            domain, dest_dir = line.strip().split(':')
            rules[domain] = dest_dir

for filename in os.listdir(downloads_dir):
    file_path = os.path.join(downloads_dir, filename)
    if os.path.isfile(file_path):
        # Get the URL from where the file was downloaded
        url = os.popen(f"mdls -name kMDItemWhereFroms '{file_path}'").read()
        if url:
            url = url.strip().strip('()"')  # Clean up the URL string
            domain = url.split("//")[-1].split("/")[0]  # Extract the domain from the URL
            if domain in rules:
                dest_dir = rules[domain]
                shutil.move(file_path, os.path.join(dest_dir, filename))  # Move the file to the destination directory
