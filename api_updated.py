# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import watson_developer_cloud
import json
import urllib2,urllib
import requests
import time
import datetime
from watson_developer_cloud import DocumentConversionV1
import requests
import pandas as pd
import csv
from watson_developer_cloud import NaturalLanguageUnderstandingV1
import watson_developer_cloud.natural_language_understanding.features.v1 as Features
from time import time
from flask import Flask, request
from flask_restful import Resource, Api
from json import dumps
from flask_cors import CORS, cross_origin
from datetime import datetime
from collections import defaultdict
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import re
import unicodedata

ins_names = {"RELIANCE":"1",	"HDFC ERGO":"2",	"ICICI LOMBARD":"3",	"Cholamandalam":"4",	"Iffco Tokio":"5",	"National Insurance":"6",	"Oriental":"8",	"Tata Aig":"9",	"ROYAL SUNDARAM":"10",	"United Insurance":"11",	"New India Assurance":"12",	"Bajaj Allianz":"13",	"Future Generali":"14",	"Shriram General Insurance":"15",	"Bharti Axa":"16",	"Universal Sompo":"17",	"Berkshire":"18",	"L&T":"21",	"SBI":"22",	"Liberty Videocon":"28",	"MAGMA":"29",	"AXA Assistance":"30",	"Allied Insurance":"31",	"Raheja QBE":"32",	"Cross Roads India Assistance Pvt Ltd":"33",	"Europ Assistance India":"34",	"Kotak General Insurance":"35"}
ignore_phone = {"8800556374"}
ignore_email = {"care@kotak.com",	"customer.service@bharti-axagi.co.in",	"crtmotor@policybazaar.com",	"nia.310300@newindia.co.in",	"fgcare@futuregenerali.in", "pb.support@uiic.co.in", "Ch31@newindia.co.in", "ch31@newindia.co.in", "Customer.service@bharti-axagi.co.in"}
ignore_name = {"Midnight Proposal", "Midnight Policy", "Agent Name"}

ins_mapping = {"Future Generali":"Future Generali",	"future generali":"Future Generali"	,	"FUTURE GENERALI":"Future Generali",		
"Bajaj Allianz":"Bajaj Allianz",	"BAJAJ ALLIANZ":"Bajaj Allianz",	"bajaj allianz":"Bajaj Allianz"	,		
"HDFC ERGO":"HDFC ERGO",	"hdfc ergo":"HDFC ERGO"	,			
"Universal Sompo":"Universal Sompo",	"universal sompo":"Universal Sompo"	,		
"United India":"United Insurance",	"united india":"United Insurance", "UNITED INDIA":"United Insurance",
"Reliance":"Reliance",	"reliance":"Reliance",				
"Iffco Tokio":"Iffco Tokio",	"ITG":"Iffco Tokio",	"iffco tokio":"Iffco Tokio"	, "IFFCO TOKIO":"Iffco Tokio", "IFFCO Tokio": "Iffco Tokio",
"Kotak":"Kotak General Insurance",	"kotak":"Kotak General Insurance"	,			
"New India Assurance":"New India Assurance",	"THE NEW INDIA ASSURANCE CO. LTD.":"New India Assurance",	"THE NEW INDIA ASSURANCE CO. LTD":"New India Assurance",	"The New India Assurance":"New India Assurance",	"new india assurance":"New India Assurance",	"the new india assurance":"New India Assurance", "NEW INDIA ASSURANCE":"New India Assurance",
"Oriental":"Oriental",	"THE ORIENTAL INSURANCE CO. LTD.":"Oriental",	"THE ORIENTAL INSURANCE CO. LTD":"Oriental",	"oriental":"Oriental",	"the oriental insurance co. ltd.":"Oriental",	
"Bharti Axa":"Bharti Axa",	"bharti axa":"Bharti Axa", "BHARTI AXA":"Bharti Axa", "Bharti AXA":"Bharti Axa",				
"Tata Aig":"Tata Aig",	"tata aig":"Tata Aig", "TATA AIG":"Tata Aig", "Tata AIG":"Tata Aig",				
"Royal Sundaram":"Royal Sundaram",	"royal sundaram":"Royal Sundaram",				
"National Insurance":"National Insurance",	"national insurance":"National Insurance", "NATIONAL INSURANCE":"National Insurance",
"Liberty Videocon":"Liberty Videocon",	"liberty videocon":"Liberty Videocon",
"ICICI Lombard General Insurance Company":"ICICI LOMBARD", "ICICI LOMBARD HOUSE":"ICICI LOMBARD", "ICICI LOMBARD GENERAL INSURANCE": "ICICI LOMBARD", "ICICI Lombard General Insurance":"ICICI LOMBARD","ICICI Lombard":"ICICI LOMBARD","ICICI Lombard House":"ICICI LOMBARD",
"Royal Sundaram":"ROYAL SUNDARAM", "ROYAL SUNDARAM":"ROYAL SUNDARAM",
"Reliance":"RELIANCE", "RELIANCE":"RELIANCE",
"UNIVERSAL SOMPO":"UNIVERSAL SOMPO"}

make_mapping = {"MAHINDRA.":"MAHINDRA AND MAHINDRA","MAHINDRA":"MAHINDRA AND MAHINDRA", "mahindra":"MAHINDRA AND MAHINDRA", "HYUNDAI MOTORS":"HYUNDAI", "MARUTI SUZUKI":"MARUTI", "MARUTI UDYOG LTD.":"MARUTI", "HYUNDAI MOTORS LTD.":"HYUNDAI"}


ig_variant_dict = ["Corporate", "Basic", "automatic", "Standard", "standard", "at"]

natural_language_understanding = NaturalLanguageUnderstandingV1(
	  username="d4f8f1c2-741c-4af0-8dcf-b9b8106538fa",
	  password="MtWIMvKCU8UY",
	  version="2017-02-27")

def build_dict(source_file):
	nested_dict = lambda: defaultdict(nested_dict)
	nest = nested_dict()
	headers = ['VehicleCode', 'Supplier', 'MakeName',	'Insurer_Model', 'Insurer_Variant', 'ins_model_variant', 'MakeId',	'ModelId',	'VariantId', 'Insurer_Make', 'ModelName', 'VariantName']
	with open(source_file, 'rb') as fp:
		reader = csv.DictReader(fp, fieldnames=headers, dialect='excel')
		for rowdict in reader:
			vehiclecode = rowdict.pop('VehicleCode')
			supplier = rowdict.pop('Supplier')
			insurer_make = rowdict.pop('MakeName')
			insurer_model = rowdict.pop('Insurer_Model')
			insurer_variant = rowdict.pop('Insurer_Variant')
			makeid = rowdict.pop('MakeId')
			modelid = rowdict.pop('ModelId')
			variantid = rowdict.pop('VariantId')
			ModelName = rowdict.pop('ModelName')
			VariantName = rowdict.pop('VariantName')
			
			nest[supplier][insurer_make][insurer_model][insurer_variant]['MakeId'] = makeid
			nest[supplier][insurer_make][insurer_model][insurer_variant]['ModelId'] = modelid
			nest[supplier][insurer_make][insurer_model][insurer_variant]['VariantId'] = variantid
			nest[supplier][insurer_make][insurer_model][insurer_variant]['ModelName'] = ModelName
			nest[supplier][insurer_make][insurer_model][insurer_variant]['VariantName'] = VariantName
			
	return dict(nest)

def build_dict_mv(source_file):
	nested_dict = lambda: defaultdict(nested_dict)
	nest = nested_dict()
	headers = ['VehicleCode', 'Supplier', 'MakeName',	'Insurer_Model', 'Insurer_Variant', 'ins_model_variant', 'MakeId',	'ModelId',	'VariantId', 'Insurer_Make', 'ModelName', 'VariantName']
	with open(source_file, 'rb') as fp:
		reader = csv.DictReader(fp, fieldnames=headers, dialect='excel')
		for rowdict in reader:
			vehiclecode = rowdict.pop('VehicleCode')
			supplier = rowdict.pop('Supplier')
			insurer_make = rowdict.pop('MakeName')
			insurer_model = rowdict.pop('Insurer_Model')
			insurer_variant = rowdict.pop('Insurer_Variant')
			ins_model_variant = rowdict.pop('ins_model_variant')
			makeid = rowdict.pop('MakeId')
			modelid = rowdict.pop('ModelId')
			variantid = rowdict.pop('VariantId')
			ModelName = rowdict.pop('ModelName')
			VariantName = rowdict.pop('VariantName')
			
			nest[supplier][insurer_make][ins_model_variant]['MakeId'] = makeid
			nest[supplier][insurer_make][ins_model_variant]['ModelId'] = modelid
			nest[supplier][insurer_make][ins_model_variant]['VariantId'] = variantid
			nest[supplier][insurer_make][ins_model_variant]['ModelName'] = ModelName
			nest[supplier][insurer_make][ins_model_variant]['VariantName'] = VariantName
			
	return dict(nest)

source_file = 'Make-Model-Variant Master.csv'
mmv = build_dict(source_file)
mmv_model_variant = build_dict_mv(source_file)
		
def get(file_path):
	with open(file_path, 'rb') as document1:
		text = document1.read()	
	new_text = text.decode('utf-8').replace('\u00a0', ' ').replace('\u00ad', ' ').replace('Â', ' ').replace('    ',' ').replace('   ',' ').replace('  ',' ')
	
	i=1
	x=0
	j=0
	store = []
	
	print "hello"
	
	previous2previous = ""
	
	chunk = 0

	prev_chunk = 0

	final_json = []
	
	while True:
		if len(new_text) - x < 10000:
			if x != prev_chunk:
				store.append(new_text[prev_chunk:x])
			store.append(new_text[x:])
			break
		else:
			x = new_text.find('\n',i)
			if x - prev_chunk > 6000:
				store.append(new_text[prev_chunk:x])
				prev_chunk = x
				chunk = chunk + 1
			else:
				i = x + 1
		j=1
	
	person_name = ""

	print datetime.now()
	
	for i in range (0, len(store)):	
		response = natural_language_understanding.analyze(text=store[i].replace('\n\n\n'," ").replace('\n\n'," ").replace('\n'," ").replace('   ',' ').replace('  ',' '),features=[Features.Entities(emotion=False,sentiment=False,limit=250,model = "20:d092ec2c-bbbd-4034-8842-f0ea13f9be45"),Features.Keywords(emotion=False,sentiment=False,limit=2)])
		final_json.append(response["entities"])

	print str(final_json)

	# field_ext = dict()

	# i=0

	# max_title = 0
	# min_email = 10000
	# max_np = 0
	# min_phone = 10000
	# max_var_len = 0
	# max_prev_insurer = 0
	# max_expiry = 0
	# flag_prev_ins = 0
	
	# for a in final_json:
	# 	for b in a:
			
	# 		if b['type'] == "previous2previous_insurer" or b['type'] == "Previous_Insurer":
	# 			temp_text = ins_mapping[b['text']]
	# 			b['text'] = temp_text
			
	# 		if b['type'] == "Make":
	# 			try:
	# 				temp_text = make_mapping[b['text']]
	# 				b['text'] = temp_text
	# 			except:
	# 				pass
			
	# 		if b['type'] == "previous2previous_insurer":
	# 			previous2previous = b['text']
	# 			flag_prev_ins = 1
			
	# 		if b['type'] == "Registration_Number":
	# 			temp_text = b['text']
	# 			b['text'] = (temp_text.replace(" ","")).replace("-","")
			
	# 		if b['type'] == "Title":
	# 			if max_title < b['count']:
	# 				max_title = b['count']
			
	# 		if b['type'] == "expiry_year":
	# 			if int(b['text']) < max_expiry:
	# 				b['type'] = "ig_expiry"
					
	# 		if b['type'] == "Email":
	# 			if b['text'] in ignore_email:
	# 				b['type'] = "ig_email"
	# 			else:
	# 				if min_email > b['count']:
	# 					min_email = b['count']

	# 		if b['type'] == "name_pattern":
	# 			if b['text'] in ignore_name:
	# 				b['type'] = "ig_name"
	# 			else:
	# 				if max_np < b['count']:
	# 					max_np = b['count']
					
	# 		if b['type'] == "Phone_Number":
	# 			if b['text'] in ignore_phone:
	# 				b['type'] = "ig_phone"
	# 			else:
	# 				if min_phone > b['count']:
	# 					min_phone = b['count']
			
	# 		if b['type'] == "Variant_Only":
	# 			if b['text'] in ig_variant_dict:
	# 				b['type'] = "ig_variant"
	# 			else:
	# 				if max_var_len < len(b['text']):
	# 					max_var_len = len(b['text'])
			
	# 		if b['type'] == "Previous_Insurer":
	# 			if max_prev_insurer < b['count']:
	# 				max_prev_insurer = b['count']
					
	# 		if b['type'] == "Full_Name" and len(b['text']) < 4:
	# 			b['type'] = "ig_name"
			
	# 		if b['type'] == "full_name_pattern" and len(b['text']) < 4:
	# 			b['type'] = "ig_name"
	# i=0
	
	# if flag_prev_ins == 1:
	# 	max_prev_insurer = 0
	
	# field_ext1 = dict()				
	# for a in final_json:
	# 	for b in a:
	# 		field_ext1[str(i)] = str(b['type'])+ "|" + str(b['count']) + "|" + b['text'] 
	# 		i=i+1

	# for a in final_json:
	# 	for b in a:			
	# 		if b['type'] == "Title" and b['count'] == max_title and b['type'] not in field_ext.keys():
	# 			field_ext[str(b['type'])] = b['text'] 
	# 		else:
	# 			if b['type'] == "Email" and b['count'] == min_email and b['type'] not in field_ext.keys():
	# 				field_ext[str(b['type'])] = b['text']
	# 			else:
	# 				if b['type'] == "name_pattern" and b['count'] == max_np and b['type'] not in field_ext.keys():
	# 					field_ext[str(b['type'])] = b['text']
	# 				else:
	# 					if b['type'] == "phone_number" and b['count'] == min_phone and b['type'] not in field_ext.keys():
	# 						field_ext[str(b['type'])] = b['text']
	# 					else:
	# 						if b['type'] == "Variant_Only" and len(b['text']) == max_var_len and b['type'] not in field_ext.keys():
	# 							field_ext[str(b['type'])] = b['text']
	# 						else:
	# 							if b['type'] == "Previous_Insurer" and b['count'] >= max_prev_insurer and b['type'] not in field_ext.keys() and b['text'] != previous2previous:
	# 								field_ext[str(b['type'])] = b['text']
	# 							else:
	# 								if b['type'] != "Title" and b['type'] != "Email" and b['type'] != "name_pattern" and b['type'] != "phone_number" and b['type'] != "Variant_Only" and b['type'] != "Previous_Insurer":
	# 									if b['type'] not in field_ext.keys():
	# 										field_ext[str(b['type'])] = b['text']

	# fm = 0
	# fm_new = 0
	# field_ext_f = field_ext
	
	# print "prev_insurer: " + field_ext_f["Previous_Insurer"]
	
	# if "Chassis_Number" in field_ext_f.keys():
	# 	field_ext_f["Chassis_Number_f"] = field_ext_f["Chassis_Number"]
	# 	#field_ext_f.pop('chassis_number_pattern')
	# else:
	# 	if "chassis_number_pattern" in field_ext_f.keys():
	# 		field_ext_f["Chassis_Number_f"] = field_ext_f["chassis_number_pattern"]
	# 		#field_ext_f.pop('chassis_number_pattern')

	# if "Engine_Number" in field_ext_f.keys():
	# 	field_ext_f["Engine_Number_f"] = field_ext_f["Engine_Number"]
	# 	#field_ext_f.pop('engine_number_pattern')
	# else:
	# 	if "engine_number_pattern" in field_ext_f.keys():
	# 		field_ext_f["Engine_Number_f"] = field_ext_f["engine_number_pattern"]
	# 		#field_ext_f.pop('engine_number_pattern')
			
	
	# if "name_pattern" in field_ext_f.keys():
	# 	field_ext_f["Customer_name"] = field_ext_f["name_pattern"].upper().replace("MR ","").replace("MR. ","").replace("MRS ","").replace("MS. ","").replace("MRS. ","")
	# 	#field_ext_f.pop('Full_Name')
	# else:
	# 	if "Full_Name" in field_ext_f.keys():
	# 		field_ext_f["Customer_name"] = field_ext_f["Full_Name"].upper().replace("MR ","").replace("MR. ","").replace("MRS ","").replace("MS. ","").replace("MRS. ","")
	# 		#field_ext_f.pop('Full_Name')
	# 	else:
	# 		if "full_name_pattern" in field_ext_f.keys():
	# 			field_ext_f["Customer_name"] = field_ext_f["full_name_pattern"].upper().replace("MR ","").replace("MR. ","").replace("MRS ","").replace("MS. ","").replace("MRS. ","")
	
	# if "Previous_Insurer_Id" not in field_ext_f.keys():
	# 	try:
	# 		field_ext_f["Previous_Insurer_Id"] = ins_names[field_ext_f["Previous_Insurer"]]
	# 	except:
	# 		field_ext_f["Previous_Insurer_Id"] = ""
	# try:
	# 	temp =  mmv[field_ext_f["Previous_Insurer"]][field_ext_f["Make"]].keys()[0]
	# 	temp2 = mmv[field_ext_f["Previous_Insurer"]][field_ext_f["Make"]][temp].keys()[0]
	# 	temp3 = mmv[field_ext_f["Previous_Insurer"]][field_ext_f["Make"]][temp][temp2]["MakeId"]
	# 	field_ext_f["Make_Id"] = temp3
	# except:
	# 	pass

	# if "model_only_pattern" in field_ext_f.keys():
	# 	field_ext_f["Model_f"] = field_ext_f["model_only_pattern"]
	# else:
	# 	if "Model_Only" in field_ext_f.keys():
	# 		field_ext_f["Model_f"] = field_ext_f["Model_Only"]
		
	
	# if "variant_only_pattern" in field_ext_f.keys():
	# 	field_ext_f["Variant_f"] = field_ext_f["variant_only_pattern"]
	# else:
	# 	if "Variant_Only" in field_ext_f.keys():
	# 		field_ext_f["Variant_f"] = field_ext_f["Variant_Only"]

	# print field_ext_f['Make']
	# print field_ext_f['Previous_Insurer']
	# if "Model_Variant" in field_ext_f.keys():
	# 	new_model, score_m = process.extractOne(field_ext_f["Model_Variant"], mmv_model_variant[field_ext_f["Previous_Insurer"]][field_ext_f['Make']].keys(), scorer=fuzz.token_sort_ratio, processor=lambda x: x)
	# 	print mmv_model_variant[field_ext_f["Previous_Insurer"]][field_ext_f['Make']].keys()
	# 	#if score_m > 20:
	# 	field_ext_f["MV_clean"] = new_model
	# 	field_ext_f["Variant_Id"] = mmv_model_variant[field_ext_f["Previous_Insurer"]][field_ext_f["Make"]][new_model]["VariantId"]
	# 	field_ext_f["Model_Id"] = mmv_model_variant[field_ext_f["Previous_Insurer"]][field_ext_f["Make"]][new_model]["ModelId"]
	# 	field_ext_f["Model_Name"] = mmv_model_variant[field_ext_f["Previous_Insurer"]][field_ext_f["Make"]][new_model]["ModelName"]
	# 	field_ext_f["Variant_Name"] = mmv_model_variant[field_ext_f["Previous_Insurer"]][field_ext_f["Make"]][new_model]["VariantName"]

	# else:
	# 	if "Model_f" in field_ext_f.keys() and "Variant_f" in field_ext_f.keys():
	# 		field_ext_f["Model_Variant_new"] = field_ext_f["Model_f"] + " " + field_ext_f["Variant_f"]
	# 		new_model, score_m = process.extractOne(field_ext_f["Model_Variant_new"], mmv_model_variant[field_ext_f["Previous_Insurer"]][field_ext_f['Make']].keys(), scorer=fuzz.token_sort_ratio, processor=lambda x: x)
	# 		print mmv_model_variant[field_ext_f["Previous_Insurer"]][field_ext_f['Make']].keys()
	# 		#if score_m > 20:
	# 		field_ext_f["MV_clean"] = new_model
	# 		field_ext_f["Variant_Id"] = mmv_model_variant[field_ext_f["Previous_Insurer"]][field_ext_f["Make"]][new_model]["VariantId"]
	# 		field_ext_f["Model_Id"] = mmv_model_variant[field_ext_f["Previous_Insurer"]][field_ext_f["Make"]][new_model]["ModelId"]
	# 		field_ext_f["Model_Name"] = mmv_model_variant[field_ext_f["Previous_Insurer"]][field_ext_f["Make"]][new_model]["ModelName"]
	# 		field_ext_f["Variant_Name"] = mmv_model_variant[field_ext_f["Previous_Insurer"]][field_ext_f["Make"]][new_model]["VariantName"]
	
	# 	else:
	# 		field_ext_f["Model_Id"] = ""
	# 		field_ext_f["Make_Id"] = ""
	# 		field_ext_f["Model_Name"] = ""
	# 		field_ext_f["Variant_Name"] = ""
	# 		field_ext_f["Make"] = ""

	# if 'email_pattern' in field_ext_f.keys():
	# 	field_ext_f["email_f"] = field_ext_f["email_pattern"]
	# else:
	# 	if 'Email' in field_ext_f.keys():
	# 		field_ext_f["email_f"] = field_ext_f["Email"]
	
	# if 'phone_pattern' in field_ext_f.keys():
	# 	field_ext_f["phone_f"] = field_ext_f["phone_pattern"]
	# else:
	# 	if 'Phone_Number' in field_ext_f.keys():
	# 		field_ext_f["phone_f"] = field_ext_f["Phone_Number"]
	
	# address_f = ""
	# add_text = new_text.replace('\n\n\n'," ").replace('\n\n'," ").replace('\n'," ").replace('   ',' ').replace('  ',' ')
	
	# if "Customer_name" not in field_ext_f:
	# 	field_ext_f["Customer_name"] = "Please Fill Info"
	
	# address_dict = {"Bajaj Allianz":["Proposer Address:", "Proposer Address :"],	"Bharti Axa": [field_ext_f["Customer_name"], "Communication Address:"], "Future Generali":["Pincode - 400013 Address :"]	,"HDFC ERGO":["Correspondence Address"]	, "Iffco Tokio":[field_ext_f["Customer_name"] + " Address:"]	, "Kotak General Insurance":[field_ext_f["Customer_name"] + " Address:"]	,"New India Assurance":[field_ext_f["Customer_name"] + " Address :", "Insureds Address:", "Insureds Address :"]	, "United Insurance":["Midnight Policy Issuing Office Address :"], "RELIANCE":["Communication Address :"],"ROYAL SUNDARAM":[field_ext_f["Customer_name"]], "Tata Aig":["Address for Communication* :"], "National Insurance":[field_ext_f["Customer_name"] + " Address :"]}	

	# print "prev_insurer: " + field_ext_f["Previous_Insurer"]
	# for add in address_dict[field_ext_f["Previous_Insurer"]]:
	# 	print add
	# 	if add_text.upper().find(add.upper(),1) > -1: 
	# 		print "Found: " + add
	# 		start = add_text.upper().find(add.upper(),1) + len(add)
	# 		print "Start: " + str(start)
	# 		break
	# 	else:
	# 		start = -1

	# if start >0:
	# 	zipcode = re.search(r'\d{6}|\d{3} \d{3}',add_text[start:]).start()
	# 	print zipcode
	# 	address_f = add_text[start:(start+zipcode)].strip().strip(",")
	# 	print address_f
	# 	if "Pincode" not in field_ext_f or len(field_ext_f["Pincode"])<6:
	# 		field_ext_f["Pincode"] = add_text[start+zipcode:(start+zipcode+7)].replace(" ","")
		
	
	# field_ext_f["Address_f"] = address_f.upper().replace("PINCODE", "").replace("PIN CODE", "").replace("COMMUNICATION ADDRESS :","")
	# print "act address" + field_ext_f["Address_f"]

	# field_ext["z_url"] = url
	# field_ext_f["z_url"] = url

	return datetime.now()
		
	# return field_ext_f

print(str(get('../data/vision/output/deskewed_text/4_2_deskewed.txt')))