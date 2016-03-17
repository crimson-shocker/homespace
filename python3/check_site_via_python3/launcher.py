#!/usr/bin/env python3

import os
import sys
import hashlib
import re
#<Internal Field Separator>
do_list = "do.list"
parent_directory = os.getcwd()
ADM_PRIV_PREFIX = "/usr/bin/python3"
hash_directory = parent_directory+'/hash/'
#</Internal Field Separator>
flag_names = ['{runonce}', '{adm_priv}']
for line in open(do_list):
	line = line.rstrip('\n')
	script_name = line.split(' ')[0]
	cmd = parent_directory+'/'+script_name
	words_count_type_list = line.split()
	words_count_type_int = len(words_count_type_list)
	param_count = words_count_type_int - 1
#<if no parameteres>
	if param_count == 0:
		os.system("%(ADM_PRIV_PREFIX)s %(cmd)s" %vars())
		continue
#</if no parameteres>
	flags = {}
#<Check provided flags>
	for flag_name in flag_names:
		found = re.findall(flag_name, line)
		param_number = len(found)
		flags[flag_name] = param_number
#</Check provided flags>
#<if run_once flag provided>
	if flags['{runonce}'] != 0:
		hash_file = hash_directory+script_name 
		hash_new = hashlib.md5(open(parent_directory+'/'+script_name, "rb").read()).hexdigest()
		if not os.path.isdir(hash_directory):
			os.mkdir(hash_directory)
			open(hash_file, "w").write("1")

		hash_old = open(hash_file, "r").read()
		if hash_new == hash_old:
			continue
		else:
			open(hash_file, "w").write(hash_new)
#</if run_once flag provided>
#<if adm_priv flag provided>
	if flags['{adm_priv}'] != 0:
		print("Do something in adm_priv blog...")
#</if adm_priv flag provided>
#<run>
	os.system("%(ADM_PRIV_PREFIX)s %(cmd)s" %vars())
#</run>	
#
