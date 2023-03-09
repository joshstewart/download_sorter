import os
import shutil
import subprocess
import re
import argparse

parser = argparse.ArgumentParser(description='Sort files based on their URLs.')
parser.add_argument('source_dir', type=str, help='path to directory containing files to be sorted')
parser.add_argument('domain_rules', type=str, help='path to file containing domain rules')
args = parser.parse_args()

# Define dictionary of domain rules
domain_dirs = {}
with open(args.domain_rules, 'r') as f:
    for line in f:
        domain, directory = line.strip().split(":")
        domain_dirs[domain] = directory

# Loop through files in source directory
for filename in os.listdir(args.source_dir):
    filepath = os.path.join(args.source_dir, filename)
    
    # Use mdls to get kMDItemWhereFroms metadata for file
    mdls_output = subprocess.check_output(["mdls", "-name", "kMDItemWhereFroms", filepath]).decode("utf-8")
    
    # Use regular expressions to extract URLs from kMDItemWhereFroms metadata
    urls = re.findall(r"https?://[^\s]+", mdls_output)
    
    # Loop through URLs and check if they match one of the domains in the list
    for url in urls:
        domain = url.split("/")[2]
        if domain in domain_dirs:
            # If a match is found, move the file to the corresponding directory
            dest_dir = domain_dirs[domain]
            print(f'Moving {filename} to {dest_dir}')
            shutil.move(filepath, os.path.join(dest_dir, filename))
            break  # Stop checking URLs once the file has been moved
