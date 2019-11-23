#!/usr/bin/env python

import os
import json
import pprint
import subprocess
import collections

dst_path = '/var/tmp/osreports'
command_dict = 'command_dict.json'

# like perl's auto-vivification for nested dicts; creates non-existent keys automatically
def makehash():
    return collections.defaultdict(makehash)
    
def run_cmd(cmd, log):
    """ Run command """
    log = dst_path + '/' + log
    p1 = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    out, err = p1.communicate()
    #print(out, end='')
    #print(err, end='')
    with open(log, 'w') as mylog:
        mylog.write(out)
        mylog.write(err)
    p1.stdout.close()
    
# Create output directory if it doesn't exist
if not os.path.exists(dst_path):
    os.makedirs(dst_path)
    
with open(command_dict, "r") as cmd_dict:
    commands = json.load(cmd_dict)

# parse command dict and run command 
for group in commands:
    for item in commands[group]:
        run_cmd(item['cmd'], item['log'])
        
# dictionary that works like a perl hash (auto-vivification)
reports = makehash()

# parse 'command' dict and populate 'reports' dict with contents of output files
for group in commands:
    for item in commands[group]:
        log = dst_path + '/' + item['log']
        with open(log, 'r') as mylog:
            #reports[group][item['title']]['cmd_title'] = item['title']
            reports[group][item['title']]['cmd_run'] = item['cmd']
            reports[group][item['title']]['cmd_log'] = log
            reports[group][item['title']]['cmd_out'] = mylog.readlines()
                           

print(json.dumps(reports, indent=4))