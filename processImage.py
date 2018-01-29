import time
import cv2 as cv
import onlineSDK as ab
import credentials as cred
import dictList as dl

class ProcessingSettings:
	Language = "English"
	OutputFormat = "txt"

AppId = "PB-OCR-TEST"
Pass = "YhSSBjPPTQaSACC7N4AYrQot" 

sett = ProcessingSettings

d_list = ['1285','1400']

for i in range(0,len(d_list)):
		img_process = ab.AbbyyOnlineSdk(cred.AppId, cred.Pass)
		name = d_list[i]
		print 'i:',i,'\n',name,'\n',"========================"
		i_image_path = '../../data_orig/small_set_for_skew/'+name+'.jpg'		
		o_xml_path = '../../data_orig/xmls/'+name+'.xml'

		o_paths = [o_xml_path]
		bodyParams = { "file" : open( i_image_path, "rb" ),
									 "language" : "English",
									 "imageSource" : "photo",
									 "profile" : "textExtraction",
									 "textType" : "ocrB",
									 "correctOrientation" : "true",
									 "exportFormat" : "xml"
									 ,"correctSkew" : "true"
									}
		urlParams = {}
		task = img_process.ProcessImage(sett, "processImage", bodyParams, urlParams)

		while True:
			print img_process.GetTaskStatus(task).DownloadUrl
			time.sleep(30)
			if len(str(img_process.GetTaskStatus(task).DownloadUrl))>30:
				break

			if img_process.GetTaskStatus(task).DownloadUrl == None:
				print img_process.GetTaskStatus(task).DownloadUrl
			else:
				break
		img_process.DownloadResult(img_process.GetTaskStatus(task), o_xml_path)


