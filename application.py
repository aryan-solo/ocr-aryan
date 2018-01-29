# -*- coding: utf-8 -*-
# while starting application on production provide env as PROD (ie. python application.py PROD)
# main application
# make sure this module imports all other python scripts and module // this is the start of the application
import sys
from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS
import watsonCallForText
import constants as c
import controller
import json
import pandas as pd
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)
@app.route('/<string:url>')
def start(url):
		url = 'http://api.policybazaar.com/cs/repo/getPolicyCopyById?docId='+url
		finalj=watsonCallForText.get(url)

		#finalj=runnuing_csv()
    #return json.dumps(finalj)
    #finalj=runnuing_csv()
		return json.dumps(finalj)


@app.route('/text/<string:url>')
def getText(url):
		url = 'http://api.policybazaar.com/cs/repo/getPolicyCopyById?docId=' + url
		return watsonCallForText.getText(url)

@app.route('/jraw/<string:url>')
def getJson(url):
		url = 'http://api.policybazaar.com/cs/repo/getPolicyCopyById?docId=' + url
		rawj=watsonCallForText.getJson(url)
		return json.dumps(rawj)
#
def getMongoConnection(env_val):
		print("=====================================")
		print("CONNECTED MONGO TO "+env_val+" SERVER")
		print("=====================================")
		flag = True
		mongodbUrl = 'mongodb://'+c.environment[env_val]['mongoHost']+':'+c.environment[env_val]['mongoPort']
		maxSevSelDelay = 1
		client = MongoClient(mongodbUrl,serverSelectionTimeoutMS=maxSevSelDelay)
		while flag:
				try:
						client.server_info()
						flag = False
				except Exception as e:
						print("error connecting to mongo:",str(e),"\n Retrying...")
		dbclient = client["ocr"]
		return dbclient


@app.route('/doc-ocr', methods = ['POST'])
def jsonImage():
		fileType = 0 #fileType is for pdf 1 and image 0
		fileCateg = 0 #fileCateg is for RC 1 and policy 0
		if 'fileType' not in request.form or 'fileCateg' not in request.form or 'file' not in request.files:
				finalj = {"error":"parameter missing please check"}
		else:
				try:
						fileType = int(request.form['fileType'])
						fileCateg = int(request.form['fileCateg'])
				except:
						pass
				file = request.files['file']
				if fileType == 1:
						finalj = controller.getJsonResponsePdf(file, mongoClient, fileCateg)
				elif fileType == 0:
						finalj = controller.getJsonResponseImage(file, mongoClient, fileCateg)
				else:
						finalj = {}
		return jsonify(finalj)

@app.route('/rc-ocr', methods = ['POST'])  # for rc data
def jsonImageRc():
        fileType = 0 #fileType is for pdf 1 and image 0
        fileCateg = 0 #fileCateg is for RC 1 and policy 0

        if 'fileType' not in request.form or 'fileCateg' not in request.form or 'file' not in request.files or 'CustomerName' not in request.form or 'MobileNumber' not in request.form or 'EmailAddress' not in request.form or 'ProductId' not in request.form or 'isClaimMade' not in request.form:

                finalj = {"error":"parameter missing please check"}
        else:
                try:
                        fileType = int(request.form['fileType'])
                        fileCateg = int(request.form['fileCateg'])
                        CustomerName=request.form['CustomerName']
                        MobileNumber= request.form['MobileNumber']
                        EmailAddress=request.form['EmailAddress']
                        ProductId=request.form['ProductId']
                        isClaimMade=request.form['isClaimMade']
                        print(type(isClaimMade))
                except:
                        pass
                file = request.files['file']
                if fileType == 1:
                        finalj = controller.getJsonResponseForRc(file, mongoClient, fileCateg,CustomerName, MobileNumber, EmailAddress, ProductId,int(isClaimMade))
                elif fileType == 0:
                        finalj = controller.getJsonResponseForRc(file, mongoClient, fileCateg,CustomerName, MobileNumber, EmailAddress, ProductId,int(isClaimMade))
                else:
                        finalj = {}
        return json.dumps(finalj)





def getOriginalData():
		originalData = pd.read_csv('../../dict/originaldata.csv')
		cols = ['Type','Registration_Number','Make','Model_Name','Variant_Name','Year_of_Manufacturing','expiry_day','expiry_month','expiry_year','Customer_name',"email_f","phone_f",'Previous_NCB','Title','Pincode','Nominee','Nominee_Age','Nominee_Relationship','Policy_Number','Engine_Number_f','Chassis_Number_f']
		return originalData[cols]


def runnuing_csv():
    df = pd.read_csv('../../dict/Samplem.csv')
    url_col = df["URLs"]
    url_ins = df["sup_name"]
    rows = [
        ['Registration_Number'],
        ['Make'],
        ['Model_Name'],
        ['Variant_Name'],
        ['Year_of_Manufacturing'],
        ['expiry_day'],
        ['expiry_month'],
        ['expiry_year'],
        ['Customer_name'],
        ["email_f"],
        ["phone_f"],
        ['Previous_NCB'],
        ['Title'],
        ['Pincode'],
        ['Nominee'],
        ['Nominee_Age'],
        ['Nominee_Relationship'],
        ['Policy_Number'],
        ['Engine_Number_f'],
        ['Chassis_Number_f'],
        ['score'],
        ['z_url']
    ]
    df_csv = pd.DataFrame(rows,columns=['Type'])

    i = 0
    localj=[]
    for a in url_col:
        i = i + 1
        print(i)
        print('\n\n')
        try:
            finalj = watsonCallForText.get(a)
            one = pd.DataFrame(finalj.items(), columns=['Type', 'Text' + str(i)])
            df_csv = pd.merge(df_csv, one, on='Type', how='outer')
            print(finalj)
            localj.append(finalj)
        except:
            sys.exc_clear()

    try:
        originalData = getOriginalData()
        filteredOriginalData = originalData.loc[originalData['Registration_Number'].isin(df_csv.iloc[0,1:].values)].T
        new_header = filteredOriginalData.iloc[0]  # grab the first row for the header
        filteredOriginalData = filteredOriginalData[1:]  # take the data less the header row
        filteredOriginalData.columns = new_header  # set the header row as the df header
        filteredOriginalData.index.name = 'Type'
        filteredOriginalData.reset_index(inplace=True)
        df_csv = pd.merge(df_csv, filteredOriginalData, on='Type', how='outer')
        df_csv.T.to_csv('Result.csv')
    except:
        pass
    return localj

if __name__ == '__main__':
		env_val = 'development'
		if len(sys.argv) == 1:
				env_val = 'development'
		else:
				env_val = c.env[sys.argv[1]]
				c.setEnvVar(sys.argv[1])
		mongoClient = getMongoConnection(env_val)
		app.run(host= '0.0.0.0',port=c.environment[env_val]['serverPort'],threaded = True)
