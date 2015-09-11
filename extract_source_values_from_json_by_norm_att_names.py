import sys
import json
from pprint import pprint

if len(sys.argv) <= 1:
	print """Usage: python extract_source_values_from_json_by_norm_att_names.py <input_json_file_name_list> <input_json_files_folder> <output_folder>

Arguments:

   <input_json_file_name_list>: A file containing the list of input files each of which cotain JSON objects of product items.

   <input_json_files_folder>: The folder containing the files with the names in <input_json_file_name_list>.

   <output_folder>: The folder to which the extracted values should be writtten. Each attribute's values are stored in a file named by the attributes name."""
	sys.exit()

values				= {}
max_prod_ids		= 20
attributes			= ['Clothing Size','Shirt Size','Waist Size','Shoe Size','Sock Size']
for att in list(attributes):
	attributes.append('Size/'+att)

yy				= 0
with open(sys.argv[1]) as g:
	for file_name in g:
		file_name			= file_name.strip()
		with open(sys.argv[2]+"/"+file_name) as f:
			for line in f:
				line			= line.strip()
				json_obj		= json.loads(line)
				if 'normalized' in json_obj:
					for att in json_obj['normalized']:
						norm_att_name		= json_obj['normalized'][att][0]['properties']['attributeName']
						if (
						       json_obj['normalized'][att][0]['properties']['attributeName'] in attributes and
						       'values' in json_obj['normalized'][att][0] and
						       'source_value' in json_obj['normalized'][att][0]['values'][0]
						   ):
							src_val			= json_obj['normalized'][att][0]['values'][0]['source_value']
							if norm_att_name not in values:
								values[norm_att_name]			= {}
							if src_val not in values[norm_att_name]:
								values[norm_att_name][src_val] = {'prod_cnt':0, 'sample_product_ids':[]}
							values[norm_att_name][src_val]['prod_cnt'] = \
							    values[norm_att_name][src_val]['prod_cnt'] + 1
							if len(values[norm_att_name][src_val]['sample_product_ids']) < max_prod_ids:
							    values[norm_att_name][src_val]['sample_product_ids'].append(json_obj['product_id'])
				yy += 1
				if yy % 1000 == 0:
					print yy

for att in values:
	att_file_name		= att.lower().replace('/','_').replace(' ', '_')
	ff		= open(sys.argv[3]+'/'+att_file_name, 'w')
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
