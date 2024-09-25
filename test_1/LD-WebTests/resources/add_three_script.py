import argparse
import csv
from schrodinger.structure import StructureReader

parser = argparse.ArgumentParser(description='Output an XKCD URL given an sd file')
parser.add_argument('--input', dest='input', help='name of sd file')
parser.add_argument('--col', dest='column', help='name of csv file with column data')
args = parser.parse_args()

filename = args.input
column = args.column
coldata = {}
with open(column) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        coldata[row['Corporate ID']] = row['Data']
print("Corporate ID,Result")
for structure in StructureReader(filename):
    corp_id = structure.property["s_sd_Corporate_ID"].strip()
    if not corp_id in coldata:
        print("%s," % corp_id)
        continue
    try:
        print("%s,%s" % (corp_id, float(coldata[corp_id]) + 3))
    except:
        print("%s,%s" % (corp_id, coldata[corp_id] + ': String'))
