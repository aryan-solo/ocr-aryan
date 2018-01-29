from google.cloud import vision
# import google.cloud.proto.vision.v1.image_annotator_pb2 as pvv
import google.cloud.vision_v1.proto.image_annotator_pb2 as pvv
import io

client = vision.ImageAnnotatorClient()

# def makeReqList(file_path):
# 	with io.open(file_path, 'rb') as image_file:
# 		content = image_file.read()
# 	im_obj = pvv.Image(content = content)
# 	return pvv.AnnotateImageRequest(image = im_obj, features = [{"type": "TEXT_DETECTION"}])
#
# def getresponse(file_path_list):
# 	req = map(makeReqList,file_path_list)
# 	response = client.batch_annotate_images(req)
# 	return response

def makeReqListImage(imageStr):
	im_obj = pvv.Image(content = imageStr)
	return pvv.AnnotateImageRequest(image = im_obj, features = [{"type": "TEXT_DETECTION"}])

def getresponseImage(imageList):
	req = map(makeReqListImage,imageList)
	response = client.batch_annotate_images(req)
	return response