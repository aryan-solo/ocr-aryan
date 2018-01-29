# using hough transform to detect if the text in the image is vertical and rotate it by 90 degrees clockwise 
# this might result an inverted image as well

import cv2
import numpy as np
from PIL import Image

def detectOrientation(img_path):
	img = cv2.imread(img_path)
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	edges = cv2.Canny(gray,50,150,apertureSize = 3)
	threshold = 300
	yes = 0
	no = 0
	lines = cv2.HoughLines(edges,1,np.pi/180,threshold)
	for line in lines[0:5]:
		for rho,theta in line:
		  a = np.cos(theta)
		  b = np.sin(theta)
		  x0 = a*rho
		  y0 = b*rho
		  x1 = int(x0 + 1000*(-b))
		  y1 = int(y0 + 1000*(a))
		  x2 = int(x0 - 1000*(-b))
		  y2 = int(y0 - 1000*(a))
		  if np.arctan(abs(y1-y0)/abs(x1-x0)) > 1 :
		  	yes +=1
		  else :
		  	no +=1
		  # cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)
	# cv2.imwrite('/home/tarunr/dev/ocr/data_orig/set_for_orientation/test.jpg',img)
	return -90 if yes > no else 0

def rotateImage(angle, img_path, o_img_path = ""):
	if o_img_path == "":
		o_img_path = img_path
	img = Image.open(img_path)
	img2 = img.rotate(angle,expand = True)
	img2.save(o_img_path)
	return 

def checkAndRotate(img_path, o_img_path = ""):
	angle = detectOrientation(img_path)
	print angle
	rotateImage(angle, img_path, o_img_path)
	return 

im_path = '/home/tarunr/dev/ocr/data_orig/set_for_orientation/'

imgs = ['56','104','235','242','246','352','353','355','356','357']
for img in imgs:
	checkAndRotate(im_path+img+'.jpg' , im_path+img+'_d.jpg')

