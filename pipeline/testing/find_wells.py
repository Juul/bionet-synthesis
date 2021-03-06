import numpy as np
import pandas as pd

import json
import os
import glob
import re

names = []
cand = []
plate = []
well = []
frag_nums = []

# Create a dictionary to link the gene name to the corresponding id number
data = pd.read_csv("./data_testing/10K_CDS.csv")
dictionary = dict(zip(data['gene_name'], data['idnum']))

previous_genes = []
for file in glob.glob("../../builds/*/build*_20*.csv"):
    print(file)
    build = pd.read_csv(file)
    previous_genes += list(build['Gene'])

for file in glob.glob("../../data/*/*.json"):
    print(file)
    with open(file,"r") as json_file:
        data = json.load(json_file)

    if data["status"]["build_ready"] == True and data["gene_id"] not in previous_genes:
    #if data["status"]["build_complete"] == "" and data["status"]["build_ready"] == True: # or data["status"]["build_complete"] == "Good_sequence":
        gene_name = data["gene_name"]
        names.append(gene_name)

print("Names: ", names)
print(len(names))

total_plates = []

for plate_map in glob.glob("../../plate_maps/*.csv"):
    details = pd.read_csv(plate_map)
    print("plate_map", plate_map)
    for index,row in details.iterrows():
        gene_name = row["customer_line_item_id"][:-2].strip()
        print(gene_name)
        total_plates.append(row["Plate"])
        if gene_name in names:
            print("match")
            cand.append(gene_name)
            plate.append(row["Plate"])
            well.append(row["Well"])

candidates = pd.DataFrame({
        "Candidate" : cand,
        "Plate" : plate,
        "Well" : well
    })

for index, row in candidates.iterrows():
    for file in glob.glob("../../data/{}/{}.json".format(dictionary[row["Candidate"]],dictionary[row["Candidate"]])):
        frag_num = 0
        print(file)
        with open(file,"r") as json_file:
            data = json.load(json_file)
        print(data["location"]["fragments"])
        for fragment in data["location"]["fragments"]:
            frag_num += 1
        frag_nums.append(str(frag_num))

candidates["Fragments"] = frag_nums

candidates = candidates[["Candidate","Plate","Well","Fragments"]]

print(candidates)

unique_plates = pd.unique(candidates["Plate"])
print(unique_plates)

remaining_per_plate = []

for plate in unique_plates:
    remaining = len(candidates[candidates.Plate == plate])
    remaining_per_plate.append(remaining)
    print("{} has {} genes left".format(plate, remaining))

plate_breakdown = pd.DataFrame({
    "Plate" : unique_plates,
    "Remaining_constructs" : remaining_per_plate
})
print(plate_breakdown)
#candidates.to_csv("./remaining_constructs.csv")


#
