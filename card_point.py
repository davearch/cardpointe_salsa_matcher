import csv
import os

FILE_DIR = 'files/'
UNKNOWNS = []


def get_salsa_d(filename: str) -> dict:
    original_salsa_d = {}
    with open(filename, encoding="utf8") as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        count = 0
        for row in csv_reader:
            original_salsa_d[count] = row
            count += 1
    return original_salsa_d


def get_cardpointe_d(filename: str) -> dict:
    with open(filename, encoding="utf8") as csv_file:
        cardpointe_d = {}
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        count = 0
        for row in csv_reader:
            cardpointe_d[count] = row
            count += 1
            # if not row['FORM_NAME (Custom Field #0)']:
            #    cardpointe_d[count] = row
            #    count += 1
    return cardpointe_d


def get_indexed_d(d: dict) -> dict:
    """ instead of an int, set the dict to be indexed by the reference number """
    # Transaction #
    # transaction pnref
    indexed_d = {}
    for _, row in d.items():
        if not row['transaction pnref']:
            raise KeyError
        val = row['transaction pnref']
        indexed_d[val] = row
    return indexed_d


def get_transactions_list(dict1: dict, dict2: dict) -> list:
    """ goes through cardpointe dict and sets the form name to what the form name is  """
    d = {}
    count = 0
    for _, row in dict1.items():
        # get transaction number (key in second dict)
        transaction_id = row['Transaction #'][1:]
        if not dict2.get(transaction_id):
            # print(transaction_id)
            UNKNOWNS.append(transaction_id)
            continue
        form = dict2[transaction_id]['activity form name']
        assert form
        # set form name in original cardpointe dict
        row['FORM_NAME (Custom Field #0)'] = form

        d[count] = row
        count += 1
    return d


def write_to_file(filename: str, transactions: list, keys) -> None:
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=keys)

        writer.writeheader()
        for _, row in transactions.items():
            writer.writerow(row)


def write_cardpointe(filename: str, transactions: dict, keys) -> None:
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=keys)

        writer.writeheader()
        for _, row in transactions.items():
            writer.writerow(row)


salsa = get_salsa_d(os.path.join(FILE_DIR, 'salsa.csv'))
cardpointe = get_cardpointe_d(os.path.join(FILE_DIR, 'Authorizations.csv'))
indexed = get_indexed_d(salsa)

l = get_transactions_list(cardpointe, indexed)
keys = l[1].keys()
write_to_file('final_cardpointe.csv', l, keys)

c_keys = cardpointe[1].keys()
write_cardpointe('old.csv', cardpointe, c_keys)


'''
unknowns = [
    "197145205377",
    "191177073782",
    "191707773671",
    "190580984182",
    "190702484044",
    "690991383816",
    "190494483675",
    "190989383472",
    "190489381741",
    "190025946460"
]
'''


def parse_dollar(amount):
    neg = False
    if amount.startswith('-'):
        neg = True
        amount = amount[1:]
    if amount.startswith('$'):
        amount = amount[1:]
    amount = amount.replace(',', '')
    try:
        output = float(amount)
        if neg:
            output = -output
        return output
    except ValueError:
        raise ValueError


batch_ids = {}
for _, r in cardpointe.items():
    for n in UNKNOWNS:
        if r['Transaction #'][1:] == n:
            date = r['Date']
            name = r['Name']
            amount = r['Amount']
            batch = r['Gateway Batch #']
            form = r['FORM_NAME (Custom Field #0)']
            print(f"{date} {name} {amount} {batch} {form}")

'''
Here is the data back formatted ready for data entry in Quickbooks. The formatting took about 75 minutes which isn't unreasonable. At least half the time was the final step of subtotaling each batch by project. I think the steps before that could be automated, but probably not that last one which involves finding the last record of a particular project, like Action Bail Fund, hitting the Sum icon and then dragging the highlighted area up to the first entry of that project. But here's the other stuff I did. You can judge whether those steps should be automated or not. 

1. Delete unneeded columns (A and B aren't needed either. I just kept them in case we needed to go back to raw data to look someone up.)
2. Sort by Batch and secondarily by Project
3. Insert 2 or 3 lines between batches

4. Total each batch (This will match deposits recorded in QB

5. Total each project within each batch
'''


"""
989 -$100.00

983 $150.00
983 $50.00
983 $35.00
983 $200.00
983 $10.00
983 $15.00
983 $40.00
983 $50.00

982 $25.00


07/14/2020 10:29:37 PM ROSALBA VARGAS -$100.00 989

07/09/2020 5:29:42 PM THEODORE T. HAJJAR $150.00 983
07/09/2020 5:27:51 PM MARGARET N. WEITZMANN $50.00 983
07/08/2020 8:23:03 PM LAURA J KAPLAN $35.00 983
07/08/2020 8:20:45 PM IGO JURGENS $200.00 983
07/08/2020 8:16:57 PM M. K. BRUSSEL $10.00 983
07/08/2020 8:14:35 PM CHRISTA GROESCHEL $15.00 983
07/08/2020 8:11:13 PM BRIAN HUTCHINSON $40.00 983
07/08/2020 7:42:21 PM LESLIE P. SALGADO $50.00 983

07/08/2020 9:54:20 AM WILL TUTTLE $25.00 982 AFGJ
"""

# todo:
# write method to compare new file with old one (sanity check)

'''
n00bs = []
for row_number, row in cardpointe.items():
    transaction_id = row['Transaction #'][1:]
    if transaction_id not in indexed:
        n00bs.append(row)
print(n00bs[0])
'''
