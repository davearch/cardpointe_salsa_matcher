import pyexcel as p
import os
FILE_DIR = 'files/'

records = p.get_records(file_name=os.path.join(FILE_DIR, 'Authorizations.csv'))

# Transaction #,Location,Date,Method,Name,Brand,Last 4,Amount,Auth Code,Status,Gateway Batch #,FORM_NAME (Custom Field #0)
for r in records:
    print(f"Transaction ID: {r['Transaction #']}, Name: {r['Name']},\t\tBatch: {r['Gateway Batch #']},\tForm: {r['FORM_NAME (Custom Field #0)']}")


my_dict = p.get_dict(file_name=os.path.join(FILE_DIR, 'Authorizations.csv'), name_columns_by_row=0)

for key, values in my_dict.items():
    print(key + " : " + ','.join([str(item) for item in values]))