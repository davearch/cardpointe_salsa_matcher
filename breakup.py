import os
import csv

def break_batches(filename: str) -> None:
    batch_d = {}
    with open(filename, encoding="utf8") as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        for row in csv_reader:
            rowList = []
            rowList.append()
            batch_id = row['Gateway Batch #']
            batch_d[batch_id] = rowList
