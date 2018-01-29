# Give input as input file path and the file is submitted 
# and it will return task object

import credentials as cred
import onlineSDK as ab

class ProcessingSettings:
	Language = "English"
	OutputFormat = "txt"

sett = ProcessingSettings

class submitImage:
	def submitImageAndGetTask(self, filePath, taskId):
		img_submit = ab.AbbyyOnlineSdk(cred.AppId, cred.Pass)
		method = "submitImage"
		bodyParams = { "file" : open(filePath, "rb" )}
		urlParams = {}
		if taskId != "" :
			bodyParams["taskId"] = taskId
		task = img_submit.ProcessImage(sett, method, bodyParams, urlParams)
		return task