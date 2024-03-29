import sys
import os
import re
import timeit

import cProfile as profile

from pprint import pprint

import json

#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#
#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#
def load_rules(rulefilename, lhs_col=1, rhs_col=2, seg_col=3, attr_col=4):
	ff				= open(rulefilename)
	attr_rule_map	= {}

	for line in ff:
		line		= line.strip()
		toks		= line.split('\t')
		
		if len(toks) > attr_col:
			try:
				rekk		= re.compile(toks[lhs_col])
			except:
				print("Skipping problematic rule (LHS: %s)"%(toks[lhs_col], ))
				continue

			if toks[attr_col] not in attr_rule_map:
				attr_rule_map[toks[attr_col]]	= {}
			attr_rule_map[toks[attr_col]][rekk]			= (toks[rhs_col], toks[seg_col])
		else:
			print "skipping line " + line
			pass

	return attr_rule_map

#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#
#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#
def apply_rules_to_values(rules, values):
	#TODO: rules format: { LHS_regex : RHS_str }
	rule_val_map		= {}
	for val in values:
		for rule in rules:
			matchobj		= rule.match(val)
			if matchobj is not None and matchobj.span() == (0,len(val)):
				if rule not in rule_val_map:
					rule_val_map[rule]		= set()
				rule_val_map[rule].add(val)

	return rule_val_map

#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#
#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#
def find_overlapping_rule_pairs(rules, values):
	#TODO: rules format: { LHS_regex : RHS_str }
	overlapping_rule_pairs		= {}
	rule_val_map				= apply_rules_to_values(rules, values)
	for rule1 in rule_val_map:
		for rule2 in rule_val_map:
			if rule1 != rule2 and rules[rule1][1] == rules[rule2][1]:
				rulepair		= (rule1, rule2) 
				revrulepair		= (rule2, rule1) 

				if rulepair not in overlapping_rule_pairs and revrulepair not in overlapping_rule_pairs:
					shks	= set(rule_val_map[rule1]) & set(rule_val_map[rule2])

					if len(shks) != 0:
						overlapping_rule_pairs[rulepair]		= shks

	return overlapping_rule_pairs

#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#
#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#
def load_values_from_json_value_file(valuefilename):
	values				= {}

	with open(valuefilename) as gg:
		for line in gg:
			json_obj		= json.loads(line)
			for kk in json_obj:
				values[kk]		= json_obj[kk]
	print("Read %d values from %s."%(len(values), valuefilename))
	return values

#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#
#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#
def load_values_from_tsv_item_file(datafilename, feat_names=['size']):
	values				= {}
	gg					= open(datafilename)
	linecnt				= 0
	itemcnt				= 0

	for line in gg:
		line		= line.strip()
		item_id		= line[0:line.find("\t")]

		for feat_name in feat_names:
			fnl		= len(feat_name)
			vals_inx	= line.find("\t%s="%(feat_name,))

			if vals_inx > -1:
				itemcnt		= itemcnt + 1
				vals_inx	= vals_inx + (fnl + 1) + 1
				vals_str	= line[vals_inx : line.find("\t", vals_inx + 1)]
				vals		= vals_str.split('__')

				for val in vals:
					if val not in values:
						values[val]		= set()
					values[val].add(item_id)
		linecnt		= linecnt + 1

	print("Extracted values from %d out of %d items read from %s."%(itemcnt, linecnt, datafilename))
	return values

#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#
#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#
#==#==#==#==#==#==#===     IGNORE FROM HERE ON! THESE ARE DEVELOPMENT TESTS.    ==#==#==#==#=#==#==#==#=#==#==#==##
#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#
#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#

if __name__ == "__main__":
	target_attribute	= 'Size/Clothing Size'
	start_time = timeit.default_timer()
	attr_rule_map				= load_rules_2(sys.argv[1])
	elapsed = timeit.default_timer() - start_time
	print(elapsed)
	start_time = timeit.default_timer()
	values						= load_values_from_tsv_item_file('wmt_all_attrs_latest.txt.have_size')
	elapsed = timeit.default_timer() - start_time
	print(elapsed)
	start_time = timeit.default_timer()
	print len(attr_rule_map[target_attribute])
	overlapping_rule_pairs		= find_overlapping_rule_pairs(attr_rule_map[target_attribute], list(values.keys()))
	elapsed = timeit.default_timer() - start_time
	print(elapsed)
	print(len(overlapping_rule_pairs))
	sortedpairs					= sorted(overlapping_rule_pairs.keys(), key=lambda x:len(overlapping_rule_pairs[x]), reverse=True)

	for (rule1,rule2) in sortedpairs:
		print (rule1.pattern + " --> " + '\n\tFOR "'.join(attr_rule_map[target_attribute][rule1]) + '"')
		print (rule2.pattern + " --> " + '\n\tFOR "'.join(attr_rule_map[target_attribute][rule2]) + '"')
		for val in overlapping_rule_pairs[(rule1,rule2)]:
			print("\t\tON %s\n-----------------===============---------------"%(val,))
