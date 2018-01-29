import onlineSDK as ab
import xml.etree.ElementTree as ET
import submitImage as submitImage
import credentials as cred
import time
class ProcessingSettings:
	Language = "English"
	OutputFormat = "xml"


sett = ProcessingSettings

class processFields:
	def getXmlFromImage(self, taskId, i_xmlFile, o_xmlFile):
		img_process = ab.AbbyyOnlineSdk(cred.AppId, cred.Pass)
		method = 'processFields'
		bodyParams = open(i_xmlFile,"rb").read()
		urlParams = { "taskId" : taskId}
		task1 = img_process.ProcessImage(sett, method, bodyParams, urlParams)
	
		while True:
			time.sleep(30)
			if len(str(img_process.GetTaskStatus(task1).DownloadUrl)) > 30 :
				break 

		img_process.DownloadResult(img_process.GetTaskStatus(task1), o_xmlFile)

		return