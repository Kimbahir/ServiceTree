# Used for command line execution
import argparse
import logging
#from app.GraphBuilder import serviceTree
from app.GraphBuilder import graphBuilder
import json

parser = argparse.ArgumentParser(description="Drawing service trees based on json data structures",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

required_flags = parser.add_argument_group('Required arguments')

required_flags.add_argument('--file', required=True,
                            default='data/datastructure.json', help="JSON file")

parser.add_argument('--output', default='output/foo.gv', help="Output file")

loglevels = dict((logging.getLevelName(level), level)
                 for level in [10, 20, 30, 40, 50])
parser.add_argument('--loglevel', default='INFO',
                    choices=list(loglevels.keys()), help="Log level")

parser.add_argument('--view', default='True',
                    choices=['True', 'False'], help="Show result")

args = parser.parse_args()

logging.basicConfig(
    level=loglevels[args.loglevel], format='%(levelname)s:\t%(message)s')

logging.debug(f'Opening {args.file}')
with open(args.file) as f:
    data = json.load(f)

logging.debug(f'Building servicetree')
g = graphBuilder()
g.loadServiceTreeFromJSON(data)

logging.debug(f'Writing/showing file')
g.drawGraph(filename=args.output, view=True)

logging.info(f'Output completed and written to {args.output}')
