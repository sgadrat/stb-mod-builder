#!/usr/bin/env python
import argparse
import json
import os
import sys

import stblib.jsonformat

# Parse command line
parser = argparse.ArgumentParser(description='Convert a STB object from JSON to DICT')
parser.add_argument('input', type=str, help='Path to the JSON object to convert')
parser.add_argument('--base-path', type=str, default=None, help='mod base directory [default: dirname of input]')
parser.add_argument('--output-format', type=str, default='dict', help='Serialization ("dict", "json") [default: %(default)s]')
args = parser.parse_args()

json_filename = args.input
base_path = args.base_path
output_format = args.output_format

# Read JSON object in a dict
with open(json_filename, 'r') as json_file:
	object_dict = stblib.jsonformat.json_to_dict(json_file, base_path)

# Serialize in JSON
if output_format == 'dict':
	sort_keys=False
	indent='  '
	print(json.dumps(object_dict, sort_keys=sort_keys, indent=indent))
elif output_format == 'json':
	#TODO make it more generic
	object_parsed = stblib.dictformat.import_from_dict(object_dict)

	char_name = object_parsed.name
	os.makedirs(f'/tmp/characters/{char_name}', exist_ok=False)
	with open(f'/tmp/characters/{char_name}/{char_name}.json', 'w') as object_file:
		stblib.jsonformat.export_to_json(object_parsed, object_file, '/tmp')
	print(f'serialized in "/tmp/characters/{char_name}/{char_name}.json"')
