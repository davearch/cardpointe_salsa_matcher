import os
import csv
import operator

with open('Authorizations.csv', encoding='utf8') as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    sortedList = sorted(csv_reader, key=operator.itemgetter(), reverse=True)