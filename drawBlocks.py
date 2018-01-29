import cv2 as cv
import xml.etree.ElementTree as ET
import visionApi
import os
import numpy as np
import organizeBlocks_v2 as oz

def getCoArrFromjson(obj):
	vertices = obj.vertices
	arr = []
	for a in vertices:
		arr.append([a.x,a.y])
	return arr

def getCoArr(xml_path):
	tree = ET.parse(xml_path)
	root = tree.getroot()

	arr = []

	for child1 in root:
		for child2 in child1:
			new = []
			if child2.attrib['blockType'] == "Text":
				new.append(int(child2.attrib['l']))
				new.append(int(child2.attrib['t']))
				new.append(int(child2.attrib['r']))
				new.append(int(child2.attrib['b']))
				arr.append(new)
	return arr

def drawAndSaveImFromVision(arr, img_path, o_img_path, name):
	img = cv.imread(img_path)
	if not os.path.exists(o_img_path):
		os.makedirs(o_img_path)
	for j in range(0,len(arr)):
		pts = np.array(arr[j],np.int32)
		pts = pts.reshape((-1,1,2))
		img = cv.polylines(img,[pts],True,(0,0,255))
		cv.imwrite(o_img_path+name+'_'+str(j)+'.jpg', img)
	return

def drawAndSaveIm(arr, img_path, o_img_path, name):
	img = cv.imread(img_path)
	# if not os.path.exists(o_img_path):
		# os.makedirs(o_img_path)
	for j in range(0,len(arr)-1):
		img = cv.rectangle(img, (arr[j][0],arr[j][1]), (arr[j][2],arr[j][3]), (0,0,155), thickness = 2)
		# cv.imwrite(o_img_path+name+'_'+str(j)+'.jpg', img)
	cv.imwrite(o_img_path+'.jpg',img)

names = ['1','2','4','11','18','22','35','38','40','57',
'64','65','67','80','87','104','107','108','109',
'110','111','114','116','120','122']

for name in names:
	xml_path = '../../data_test/xmls/'+name+'.xml'
	img_path = '/home/tarunr/dev/ocr/data_test/images/'+name+'.jpg'
	o_img_path = '../../data_test/draw/'+name

	# Arr = getCoArr(xml_path)
	Arr = oz.main(xml_path)
	drawAndSaveIm(Arr, img_path, o_img_path, name)



