from tinydb import TinyDB
import csv
import os

db = TinyDB('db.json')

with open('test_dataset\\camera8_boxes.csv', 'r') as f:
    csv_reader = csv.DictReader(f)
    line_count = 0
    
    spots = []
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        
        crop_arr = [int(int(row["X"]) / 2.6) , int(int(row["Y"]) / 2.6), int(int(row["W"]) / 2.6), int(int(row["H"]) / 2.6)]
        custom_dict = dict()
        custom_dict["slot_id"] = row["SlotId"]
        custom_dict["crop"] = crop_arr
        custom_dict["occupied"] = False
        spots.append(custom_dict)
        line_count += 1

global test_dataset
test_images = os.listdir('test_dataset/S/')
for img_url in test_images:
    db.insert({"weather": "S", "url": img_url, "spots": spots})

db.close()