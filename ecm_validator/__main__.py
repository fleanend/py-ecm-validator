import xtm_parser
import xtm_validator
import sys
import codecs
import argparse

reload(sys)
sys.setdefaultencoding('utf-8')

parser = argparse.ArgumentParser("Arguments for parser")
parser.add_argument("--debug", help="Debug flag", action="store_true")
parser.add_argument("-f", "--file", help="Input file", required=True)

args = parser.parse_args()
debug = args.debug
filename = args.file

with codecs.open(filename, "r", "utf-8") as data:
	print "Parsing file %(filename)s..." % locals()
	root = xtm_parser.xml_parse(data.read(), debug=debug)
	print "Validating file %(filename)s..." % locals()
	print xtm_parser.tree(root)
	xtm_validator.validate_constraints(root)