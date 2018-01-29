import xml.etree.ElementTree as ET
import xmljson
import time
import submitImage as submitImage
import processFields as processFields

def getInputXmlForFields(i_xml_path, name):

	tree2 = ET.parse('2example.xml')
	root2 = tree2.getroot()

	##################here we are making the fieldTemplate model for text#############
	page = root2.find('{http://ocrsdk.com/schema/taskDescription-1.0.xsd}page')

	###################################################################################

	tree = ET.parse(i_xml_path)
	root = tree.getroot()

	arr = []
	count = 0
	for child1 in root:
		for child2 in child1:
			count = count+1
			new = ET.Element('text')
			new.set('template',"textField")
			new.set('id','field'+str(count))
			if child2.attrib['blockType'] == "Text":
				new.set('left',child2.attrib['l'])
				new.set('top',child2.attrib['t'])
				new.set('right',child2.attrib['r'])
				new.set('bottom',child2.attrib['b'])
				page.append(new)

	output_xml = '../data/xml/output/'+name+'_input_processFields.xml'
	tree2.write(output_xml, xml_declaration=True, encoding='UTF-8', method="xml")
	with open(output_xml,'rb') as a:
		word = re.sub('',' ', a.read())
	return output_xml


for i in range(1,2):
	for j in range(1,2):
		name = str(i)+'_'+str(j)
		filePath = '../data/Deskewed_original/'+name+'.jpg'
		i_xml_path = '../data/xml/original/'+name+'.xml'
		o_xml_path = '../data/xml/original/'+name+'_output_processfields.xml'
		# xml_file = getInputXmlForFields(i_xml_path,name)
		
		xml_file = '../data/xml/output/send_input_processFields.xml'

		img_submit = submitImage.submitImage()
		task = img_submit.submitImageAndGetTask(filePath,"")
		
		print task.Id, xml_file

		img_process = processFields.processFields()
		img_process.getXmlFromImage(task.Id, xml_file, o_xml_path)
