import credentials as CRED
from cloudOcr import CloudOCR

ocr_engine = CloudOCR(CRED.AppId, CRED.Pass)


def detectBlock(i_image_path):
		bodyParams = {
									 "imageSource" : "photo",
									 "profile" : "textextraction",
									 "textType" : "normal",
									 "correctOrientation" : "false",
									 "exportFormat" : "xml",
									 "correctSkew" : "false",
									 "readBarcodes" : "false"
									}
		post_file = {'file':open(i_image_path,"rb")}
		task = ocr_engine.processImage(post_file, **bodyParams)
		return task

def getXmlAndSave(task, delay_between_status_check, timeout, o_xml_path):
		result = ocr_engine.download(task, delay_between_status_check, timeout)
		for format, content in result.items():
				output_filename = o_xml_path
				with open(output_filename, 'wb') as output_file:
						output_file.write(content.read())
						output_file.close()
				if format == 'xml':
						xmlbuffer = content.read()
		return xmlbuffer
