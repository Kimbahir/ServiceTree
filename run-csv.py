# Used for command line execution
import argparse
import logging
#from app.GraphBuilder import serviceTree
from app.GraphBuilder import graphBuilder
import json

parser = argparse.ArgumentParser(description="Return server list from CSV file",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

required_flags = parser.add_argument_group('Required arguments')

required_flags.add_argument('--file', required=True, help="CSV file")

#parser.add_argument('--output', default='output/foo.gv', help="Output file")

loglevels = dict((logging.getLevelName(level), level)
                 for level in [10, 20, 30, 40, 50])
parser.add_argument('--loglevel', default='INFO',
                    choices=list(loglevels.keys()), help="Log level")

#parser.add_argument('--view', default='True', choices=['True', 'False'], help="Show result")

args = parser.parse_args()

logging.basicConfig(
    level=loglevels[args.loglevel], format='%(levelname)s:\t%(message)s')

logging.debug(f'Opening {args.file}')
with open(args.file) as f:
    data = f.readlines()

logging.debug(f'Getting CSV output')
g = graphBuilder()
result = g.getServiceArrayFromCSV(data)

logging.debug(f'Writing output')
print(result)
