
import sys
import os
sys.path.insert(0, '/home/aryan/ocr/lib/services')
sys.path.insert(0, '/home/aryan/ocr/lib/abby')
sys.path.insert(0, '/home/aryan/ocr/lib/vision')
sys.path.append('/usr/local/lib/python3.5/dist-packages')
import json
from random import randint
import blockDetection as BD
import organizeBlocks as OZ
import visionMain as VA
import cropAndSave as CAS
import watsonCallForNlu as WCN
import watsonCallForText as WCT
import databaseServices as DBServices
import jsonParser
import rcJsonParser
import datetime
import rcJsonParser2w


xmlPath = '/home/aryan/ocr/data_temp/temp/'
imgPath = '/home/aryan/ocr/data_temp/temp/'
txtPath = '/home/aryan/ocr/data_temp/temp/'
pdfPath = '/home/aryan/ocr/data_temp/temp/temp.pdf'

def uploadDoc(docPath):
		response = DBServices.uploadDoc(docPath)
		print("DB upload",datetime.datetime.now())
		r = response._content
		r = str(r,'utf-8')
		rjson = json.loads(r)
		try:
			docId = str(rjson[u'policyCopyDetails'][u'policyDocUrl'])
		except:
			docId=" "
		print(docId)
		return docId
# imgFullPath, dbClient, fileCateg,CustomerName, MobileNumber, EmailAddress, ProductId
def uploadDocRc(img, dbClient, fileCateg,CustomerName,MobileNumber,EmailAddress,ProductId,isClaimMade):
		print("in controller before db service")
		response = DBServices.uploadDocRc(img,dbClient, fileCateg,CustomerName,MobileNumber,EmailAddress,ProductId,isClaimMade)
		print("DB upload",datetime.datetime.now())
		r = response._content
		r = str(r,'utf-8')
		rjson = json.loads(r)
		try:
			docId = str(rjson[u'policyCopyDetails'][u'policyDocUrl'])
		except:
			docId=" "
		print(docId)
		print("point 2")
		return docId




def getJsonResponseImage(img, dbClient, fileCateg):
		updObj = dict()
		name = str(randint(1000000, 9999999))
		print("====================================================")
		print("started processing IMAGE ",name," at : ",datetime.datetime.now())
		imgFullPath = imgPath+name+'.jpg'
		xmlFullPath = xmlPath+name+'.xml'
		txtFullPath = txtPath+name+'.txt'
		img.save(imgFullPath) #saving image to path
		try:
				print("post to abby")
				task = BD.detectBlock(imgFullPath)
				print("back from abby :",datetime.datetime.now())
				
				imageId = uploadDoc(imgFullPath)
				DBServices.uploadFileToMongo("ocr_data", imageId, fileCateg, 0, dbClient)
				print("received Id going to abby at :",datetime.datetime.now())

				xmlbuffer = BD.getXmlAndSave(task, 5, 300, xmlFullPath)
				updObj['xml'] = str(xmlbuffer)
				print("after Abby before vision:",datetime.datetime.now())

				Coarr = OZ.organize(xmlFullPath)
				buffArr = CAS.cropImageAndretArrPIL(imgFullPath, Coarr)
				text_final = VA.getTextForImage(buffArr, txtFullPath)
				print(text_final,"\nafter vision beofre watson:",datetime.datetime.now())
				updObj['text'] = text_final

				watsonJson = WCN.getJsonFromWatson(txtFullPath)
				updObj['watsonRes'] = watsonJson
				print("after watson before parser",datetime.datetime.now())

				if fileCateg == 0:
					finalJson = jsonParser.parser( watsonJson,textPath=txtFullPath)
				elif fileCateg == 1:
					finalJson = rcJsonParser.parser(txtFullPath, watsonJson)
				elif fileCateg == 2:
					finalJson = rcJsonParser2w.parser(txtFullPath,watsonJson)
				else:
					finalJson = {}
				updObj['parser'] = finalJson
		except Exception as e:
				print("error occured Please check", str(e))
				finalJson = {}
		finally:
				print(finalJson,"made final json and saved in mongo:",datetime.datetime.now())
				DBServices.updateObjInMongo("ocr_data", updObj, imageId, dbClient)
				try:
						os.remove(imgFullPath)
						os.remove(xmlFullPath)
						os.remove(txtFullPath)
				except:
						pass
		return finalJson


def getJsonResponsePdf(pdf_file, dbClient, fileCateg):
		updObj = dict()
		name = str(randint(1000000, 9999999))
		pdfFullPath = pdfPath+name+'.pdf'
		txtFullPath = txtPath+name+'.txt'
		print("===================================================")
		print("started processing PDF ",name," at:",datetime.datetime.now())
		pdf_file.save(pdfFullPath) #saving pdf to path
		pdfId = uploadDoc(pdfFullPath)
		try:	
				DBServices.uploadFileToMongo("ocr_data", pdfId, fileCateg, 1, dbClient)
				print("received Id going to watson document converter:",str(pdfId))

				text = WCT.get(pdfFullPath)
				store = WCT.Chunks_of_text(text)

				print("received text going to watson nlu")
				# updObj['text'] = text
				watsonJson = WCN.call_to_nlu(store)
				print("received watson response going to json/rc parser")
				updObj['watsonRes'] = watsonJson
				if fileCateg == 0:
						text = " ".join(store)
						finalJson = jsonParser.parser(watsonJson,text=text)
				elif fileCateg == 1:
						finalJson = rcJsonParser.parser(txtFullPath,watsonJson)
				elif fileCateg ==2:
						finalJson = rcJsonParser2w.parser(txtFullPath,watsonJson)
				else:
						finalJson = {}
				updObj['parser'] = finalJson
		except Exception as e:
				print("error occured Please check", str(e))
				finalJson = {}
				
		finally:
				print(finalJson,"made final json and saved in mongo:",datetime.datetime.now())
				DBServices.updateObjInMongo("ocr_data", updObj, pdfId, dbClient)
				try:
						os.remove(pdfFullPath)
						os.remove(txtFullPath)
				except:
						pass
		return finalJson


def getJsonResponseForRc(img, dbClient, fileCateg,CustomerName,MobileNumber,EmailAddress,ProductId,isClaimMade):
		updObj = dict()
		name = str(randint(1000000, 9999999))
		print("====================================================")
		print("started processing IMAGE ",name," at : ",datetime.datetime.now())
		imgFullPath = imgPath+name+'.jpg'
		xmlFullPath = xmlPath+name+'.xml'
		txtFullPath = txtPath+name+'.txt'
		img.save(imgFullPath) #saving image to path
		try:
				print("post to abby")
				task = BD.detectBlock(imgFullPath)
				print("back from abby :",datetime.datetime.now())
				imageId = uploadDoc(imgFullPath)
				print("after this")
				try:
						imageIdRc = uploadDocRc(imgFullPath, dbClient, fileCateg,CustomerName, MobileNumber, EmailAddress, ProductId,isClaimMade)
						print("point 1",imageIdRc)
				except Exception as e:
						print("upload failde",str(e))
						pass
				# twUploadId=uploadDoc(imgFullPath,fileCateg)
				# img, dbClient, fileCateg, CustomerName, MobileNumber, EmailAddress, ProductId

				DBServices.uploadFileToMongo("ocr_data", imageId, fileCateg, 0, dbClient)
				print("received Id going to abby at :",datetime.datetime.now())

				xmlbuffer = BD.getXmlAndSave(task, 5, 300, xmlFullPath)
				updObj['xml'] = str(xmlbuffer)
				print("after Abby before vision:",datetime.datetime.now())

				Coarr = OZ.organize(xmlFullPath)
				buffArr = CAS.cropImageAndretArrPIL(imgFullPath, Coarr)
				text_final = VA.getTextForImage(buffArr, txtFullPath)
				print(text_final,"\nafter vision beofre watson:",datetime.datetime.now())
				updObj['text'] = text_final

				watsonJson = WCN.getJsonFromWatson(txtFullPath)
				updObj['watsonRes'] = watsonJson
				print("after watson before parser",datetime.datetime.now())

				if fileCateg == 0:
					finalJson = jsonParser.parser( watsonJson,textPath=txtFullPath)
				elif fileCateg == 1:
					finalJson = rcJsonParser.parser(txtFullPath, watsonJson)
				elif fileCateg == 2:
					finalJson = rcJsonParser2w.parser(txtFullPath,watsonJson)
				else:
					finalJson = {}
				updObj['parser'] = finalJson
		except Exception as e:
				print("error occured Please check", str(e))
				finalJson = {}
		finally:
				print(finalJson,"made final json and saved in mongo:",datetime.datetime.now())
				DBServices.updateObjInMongo("ocr_data", updObj, imageId, dbClient)
				try:
						os.remove(imgFullPath)
						os.remove(xmlFullPath)
						os.remove(txtFullPath)
				except:
						pass
		return finalJson
