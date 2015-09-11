from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.template.context_processors import csrf
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt

from . import rule_overlaps
from pprint import pprint
import ConfigParser

import ast
import json
import pdb
import timeit
import sys, os
import traceback

#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#
#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#
@csrf_exempt
def index(request):
	context 					= {}
	conf						= ConfigParser.ConfigParser()
	conf.read('rule_overlap.cfg')
	source_att_names			= [fname for fname in os.listdir(conf.get('INPUT', 'value_file_directory'))]
	context['source_att_names']	= source_att_names
	attr_rule_map				= rule_overlaps.load_rules(conf.get('INPUT', 'rule_file'))
	atts_to_rem					= []
	for rule_att in attr_rule_map:
		fnd		= False
		lower_rule_att		= rule_att.lower().replace(' ', '_').replace('/', '_')
		for source_att in source_att_names:
			if source_att in lower_rule_att:
				fnd		= True
		if not fnd:
			atts_to_rem.append(rule_att)
	for rmatt in atts_to_rem:
		del attr_rule_map[rmatt]
	context['attr_rule_map']	= attr_rule_map
	return render(request, 'rule_overlap/index.html', context)

#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#
#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#==#
# @ensure_csrf_cookie
@csrf_exempt
def find(request):
	context 					= {}
	conf						= ConfigParser.ConfigParser()
	conf.read('rule_overlap.cfg')
	if request.is_ajax():
		if sys.version_info[0] == 3:
			post			= ast.literal_eval(request.body.decode("utf-8"))
		else:
			post			= ast.literal_eval(request.body)
		prodattr		= post['prodattr']
		ruleattr		= post['ruleattr']
		ruleattr		= ruleattr.split('[')
		ruleattr		= ruleattr[0].strip()

		res 			= ""

		try:
			start_time = timeit.default_timer()
			attr_rule_map				= rule_overlaps.load_rules(conf.get('INPUT', 'rule_file'))
			elapsed = timeit.default_timer() - start_time
			print(elapsed)
			start_time = timeit.default_timer()
			values						= rule_overlaps.load_values_from_json_value_file(conf.get('INPUT', 'value_file_directory')+'/'+prodattr)
			elapsed = timeit.default_timer() - start_time
			print(elapsed)
			start_time = timeit.default_timer()
			overlapping_rule_pairs		= rule_overlaps.find_overlapping_rule_pairs(attr_rule_map[ruleattr], list(values.keys()))
			elapsed = timeit.default_timer() - start_time
			print(elapsed)
		except:
			traceback.print_exc()
			raise

		sortedpairs					= sorted(overlapping_rule_pairs.keys(), key=lambda x:len(overlapping_rule_pairs[x]), reverse=True)

		print(len(sortedpairs))
		for (rule1,rule2) in sortedpairs:
			res = res + "<tr><td><b>Rule 1</b>: %s <b>--></b> %s [[Segment: %s]]</td><td></td><td></td></tr>"%(str(rule1.pattern), str(attr_rule_map[ruleattr][rule1][0]), str(attr_rule_map[ruleattr][rule1][1])) 
			res = res + "<tr><td><b>Rule 2</b>: %s <b>--></b> %s [[Segment: %s]]</td><td></td><td></td></tr>"%(str(rule2.pattern), str(attr_rule_map[ruleattr][rule2][0]), str(attr_rule_map[ruleattr][rule2][1])) 
			for val in overlapping_rule_pairs[(rule1,rule2)]:
				res 			= res + "<tr><td></td><td><i><b>%s</b></i></td><td><i><b>%d items</b></i></td></tr>"%(val, values[val]['prod_cnt'])
		context['attr_rule_map']	= res

	context['success']			= True
	return HttpResponse(json.dumps(context), content_type="application/json; charset=utf-8")
