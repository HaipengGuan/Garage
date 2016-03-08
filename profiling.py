#!/usr/bin/env python
__author__ 		= "Haipeng Guan"
__email__ 		= "guanhaipeng@gmail.com"

from pymongo import MongoClient
import matplotlib.pyplot as plt
import csv
import json
from datetime import datetime


# --------------------------------------------------
# # # # # # # # Configuration # # # # # # # # # # #
# --------------------------------------------------

host = '127.0.0.1'
port = 27017
# find all operation info from this collection
db_name 	= 'testing'
coll_name 	= 'intense_testing'
MongoDB_URL = 'mongodb://localhost'

# the field that you are interested in. add if you want more
# it's also the header in csv file.
target_fields = [ 'op', 'ns', 'query', 'nreturned', 'millis', 'ts', 'client', 'execStats']


csv_outfile  = 'profile_info.csv'
json_outfile = 'profile_info.json'

# the maximum number of results to return. 0 = all results
profile_limit = 0

connect_to_db = False

bins = 50

# operation type that is going to display
display_op = [
	'find',
	'insert',
	'update',
]




# --------------------------------------------------
# # # # # # # # # # Methods # # # # # # # # # # #
# --------------------------------------------------

def is_display_op(query_dict):
	for op in display_op:
		if op in query_dict:
			return True
	return False

def connectDB():
	print 'connect to database'
	try:
		client = MongoClient(MongoDB_URL)
	except Exception, e:
		print 'failed to connect to database: %s' % str(e)
		exit()
	return client

# search index information in a dict
def findIXSCAN(data):
	if not 'stage' in data:
		return ['no-stage', 'empty']
	elif data['stage'] == 'IXSCAN':
		return ['IXSCAN', data['keyPattern']]
	elif 'inputStage' in data:
		return findIXSCAN(data['inputStage'])
	else:
		return ['COLLSCAN', 'empty']

# Decode Unicode values.
def byteify(input):
	if isinstance(input, dict):
		return {byteify(key):byteify(value) for key,value in input.iteritems()}
	elif isinstance(input, list):
		return [byteify(element) for element in input]
	elif isinstance(input, unicode):
		return input.encode('utf-8')
	else:
		return input

def field_filter(data):
	# print 'choose target fields ...'
	temp_filed = filter(lambda x: x in data, target_fields)
	# Not every profile includes all target_fields
	if len(temp_filed) < len(target_fields):
		not_fount = filter(lambda x: not x in temp_filed, target_fields)
		print 'Unable to find fields: %r in operation type: [%s]' % (not_fount, data['op'])
	return {field: data[field] for field in temp_filed}



# --------------------------------------------------
# # # # # # # # Main function # # # # # # # # # # #
# --------------------------------------------------

if __name__ == '__main__':
	if connect_to_db:
		client = connectDB()
		db = client[db_name]
		print 'reading system.profile'
		profile_raw_data = db.system.profile.find({"ns" : '.'.join([db_name, coll_name])}, limit=profile_limit)
		filter_data = map(field_filter, profile_raw_data)
		# add index information after searching IXSCAN in "execStats"
		# if cannot find: None
		epoch = datetime.fromtimestamp(0)
		start_dtime = min([elem['ts'] for elem in filter_data])
		for elem in filter_data:
			[elem['stage'], elem['keyPattern']] = findIXSCAN(elem['execStats'])
			elem['ts_str'] = str(elem['ts'])
			elem['delta_sec'] = (elem['ts'] - start_dtime).total_seconds()
			del elem['ts']

		print 'saving CSV files'
		with open(csv_outfile, 'w') as f:
			f_csv = csv.DictWriter(f, filter_data[0].keys(), dialect=csv.excel)
			f_csv.writeheader()
			f_csv.writerows(byteify(filter_data))
		print 'saving json files'
		with open(json_outfile, 'w') as f:
			json.dump(filter_data, f, indent=4)
	else:
		with open(json_outfile, 'r') as f:
			filter_data = json.load(f)
	time_stamps = []
	for elem in filter_data:
		if is_display_op(elem['query']):
			time_stamps.append(elem['delta_sec'])
	plt.hist(time_stamps, bins, histtype = 'step')
	plt.xlabel('time (sec)')
	plt.ylabel('number of query')
	# plt.title(title)
	plt.legend()
	plt.show()

