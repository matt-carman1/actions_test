import argparse
import random

from schrodinger.structure import StructureReader

parser = argparse.ArgumentParser(description='Output Random numbers given an sd file')
parser.add_argument('--input', dest='input', help='name of sd file')

args = parser.parse_args()

filename = args.input
print("Corporate ID,Result")
for structure in StructureReader(filename):
    print("%s,%s" % (structure.property["s_sd_Corporate_ID"].strip(), random.randrange(5, 120, 1)))
