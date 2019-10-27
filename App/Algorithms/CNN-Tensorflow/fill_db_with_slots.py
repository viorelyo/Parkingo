from tinydb import TinyDB
import csv

db = TinyDB('db.json')

with open('dataset\\camera8.csv', 'r') as f:
    csv_reader = csv.DictReader(f)
    line_count = 0
    
    spots = []
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        
        crop_arr = [int(int(row["X"]) / 2.6) , int(int(row["Y"]) / 2.6), int(int(row["W"]) / 2.6), int(int(row["H"]) / 2.6)]
        custom_dict = dict()
        custom_dict["crop"] = crop_arr
        custom_dict["occupied"] = False
        spots.append(custom_dict)
        line_count += 1

db.insert({"url": "2015-11-12_1019.jpg", "spots": spots})
db.close()