from datetime import datetime
start = datetime.now()
print("Starting run at: ",start)

import numpy as np
import pandas as pd

import json
import os
import glob
import re
import math

import collections

import shutil
from config import *


import_time = datetime.now()
print("Time to import: ",import_time - start)

PIPELINE_PATH = BASE_PATH + "/pipeline"
BUILDS_PATH = BASE_PATH + "/builds"
DATA_PATH = BASE_PATH + "/data"

BACKBONE_PATH = BASE_PATH + "/sequencing_files/popen_v1-1_backbone.fasta"
DICTIONARY_PATH = PIPELINE_PATH + "testing/data_testing/10K_CDS.csv"

outcome = []

build_num = "build"+str(input("Which build: ")).zfill(3)
print("build_num",build_num)

SEQFILE_PATH = "{}/{}/{}_seq_files".format(BUILDS_PATH,build_num,build_num)

RESULTS_PATH = "{}/{}/{}_alignment_results.csv".format(BUILDS_PATH,build_num,build_num)

results = pd.read_csv(RESULTS_PATH)
print(results)

for index, row in results.iterrows():
    outcome.append(row["Outcome"])

    with open("{}/{}/{}.json".format(DATA_PATH,row["Gene ID"],row["Gene ID"]),"r") as json_file:
        data = json.load(json_file)
    for attempts in data["status"]["build_attempts"]:
        attempts["build_outcome"] = row["Outcome"]
    data["status"]["build_complete"] = row["Outcome"]

    with open("{}/{}/{}.json".format(DATA_PATH,row["Gene ID"],row["Gene ID"]),"w+") as json_file:
        json.dump(data,json_file,indent=2)

print(outcome)

counter = collections.Counter(outcome)
counter = dict(counter)
outcomes = list(counter.keys())
counts = list(counter.values())
print(counter)

stats = pd.DataFrame({
    'Outcome' : outcomes,
    'Count' : counts
 })

total = stats['Count'].sum()

stats['Percentage'] = (stats['Count'] / total) * 100

stats = stats[['Outcome','Count','Percentage']]

print("total:", stats['Count'].sum())

print(stats)


stop = datetime.now()
runtime = stop - start
print("Total runtime is: ", runtime)






#
