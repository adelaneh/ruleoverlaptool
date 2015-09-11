import sys
import codecs

outfile		= open(sys.argv[2], 'w')

with open(sys.argv[1]) as f:
	next(f)
	for line in f:
		line			= line.strip()
		toks			= line.split('\t')
		try:
			if toks[2].lower() == 'mapping':
				rule_id			= toks[0]
				rule_str		= toks[1]
				rule_type		= toks[2]
				rule_format		= toks[3]
				rule_context	= toks[32]
				rule_att		= toks[33]

				rule_str_toks	= rule_str.split('||')
				rule_lhs		= rule_str_toks[0]
				rule_rhs		= rule_str_toks[1]
				rule_segment	= rule_str_toks[2]
				outfile.write("%s\n"%('\t'.join([rule_id, rule_lhs, rule_rhs, rule_segment, rule_att, rule_type, rule_context, rule_format]), ))
		except:
			print sys.exc_info()[0]
			print line+"\n==========================="

outfile.close()
