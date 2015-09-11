import sys
import json
from pprint import pprint

if len(sys.argv) <= 1:
	print """Usage: python extract_normalized_values_from_json.py <input_json_file_name_list> <input_json_files_folder> <output_folder>

Arguments:

   <input_json_file_name_list>: A file containing the list of input files each of which cotain JSON objects of product items.

   <input_json_files_folder>: The folder containing the files with the names in <input_json_file_name_list>.

   <output_folder>: The folder to which the extracted values should be writtten. Each attribute's values are stored in a file named by the attributes name in all lower case and with spaces replaced by '_'s."""

	sys.exit()

values				= {}
max_prod_ids		= 20
att_names			= ['Animal Lifestage','Bed Pillow Size','Bed Size','Bed Type','Brand','Carats','Category','Clothing Size','Fabric Material','Finish','Form','Gender','Lifestage','Material','Microwave Oven Type','Mobile Operating System','Pattern','Photo Size','Shirt Size','Shoe Size','Skin Type','Theme','Type','Watts']

attributes			= []
for att_name in att_names:
	attributes.append(att_name.lower().replace(' ', '_'))

yy				= 0
with open(sys.argv[1]) as g:
	for file_name in g:
		file_name			= file_name.strip()
		with open(sys.argv[2]+"/"+file_name) as f:
			for line in f:
				line			= line.strip()
				json_obj		= json.loads(line)
				for att in attributes:
					if (
					       'normalized' in json_obj and 
					       att in json_obj['normalized'] and
					       'values' in json_obj['normalized'][att][0] and
					       'value' in json_obj['normalized'][att][0]['values'][0]
					   ):
						if att not in values:
							values[att]			= {}
						if json_obj['normalized'][att][0]['values'][0]['value'] not in values[att]:
							values[att][json_obj['normalized'][att][0]['values'][0]['value']] = {'prod_cnt':0, 'sample_product_ids':[]}
						values[att][json_obj['normalized'][att][0]['values'][0]['value']]['prod_cnt'] = \
						    values[att][json_obj['normalized'][att][0]['values'][0]['value']]['prod_cnt'] + 1
						if len(values[att][json_obj['normalized'][att][0]['values'][0]['value']]['sample_product_ids']) < max_prod_ids:
						    values[att][json_obj['normalized'][att][0]['values'][0]['value']]['sample_product_ids'].append(json_obj['product_id'])
				yy += 1
				if yy % 1000 == 0:
					print yy
for att in values:
	ff		= open(sys.argv[3]+'/'+att, 'w')
	for (kk,vv) in values[att].items():
		ff.write(json.dumps(dict([(kk,vv)])))
		ff.write('\n')
	ff.close()
#for (kk,vv) in values.items():
#	print(json.dumps(dict([(kk,vv)])))
#print(json.dumps(values))
#			print json_obj['normalized']['size'][0]['values'][0]['source_value']
#		pprint(json_obj)
#		print("=====================================================================================================================")
#		print("=====================================================================================================================")
#		print("=====================================================================================================================")
