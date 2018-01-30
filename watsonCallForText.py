# -*- coding: utf-8 -*-

# method to convert pdf to text by calling the watson api
#import sys
#import importlib
#importlib.reload(sys)
#sys.setdefaultencoding("utf-8")
import watson_developer_cloud
import urllib
# import urlparse
from watson_developer_cloud import DocumentConversionV1
import watsonCallForNlu
import config
# from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
# from pdfminer.converter import TextConverter, XMLConverter
# from pdfminer.layout import LAParams
# from pdfminer.pdfpage import PDFPage
# from cStringIO import StringIO



document_conversion = watson_developer_cloud.DocumentConversionV1(username='your-ibm-bluemix-account',
                                                                  password='****', version='2015-12-15')

def geturl(Address, FileName):
    html_data = urllib.urlopen(Address).read()  # Open the URL
    with open(FileName, 'w+b') as f:  # Open the file
        f.write(html_data)  # Write data from URL to file


def get(pdfPath):
  # parsed = urlparse.urlparse(url)
  # docId = urlparse.parse_qs(parsed.query)['docId'][0]
  # print "Processing docId: "+docId
  # geturl(url,config.dictPath+docId+".pdf")

  with open(pdfPath, 'rb') as document1:
      config1 = {'conversion_target': DocumentConversionV1.NORMALIZED_TEXT}
      text = (document_conversion.convert_document(document=document1, config=config1, media_type='application/pdf').content)
      #new_text = text.decode('utf-8').replace('\u00a0', ' ').replace('\u00ad', ' ').replace('Â', ' ').replace('    ',' ').replace('   ', ' ').replace('  ', ' ').replace('\u20b9',' ').replace('\ufffd',' ').replace('\u037e',' ').replace('\u2022',' ').replace('\u200b',' ')
      # print text
  return text


# def getText(url):
#   parsed = urlparse.urlparse(url)
#   docId = urlparse.parse_qs(parsed.query)['docId'][0]
#   print("Processing docId: " + docId)
#   geturl(url, config.dictPath + docId + ".pdf")

#   with open(config.dictPath+docId+'.pdf', 'rb') as document1:
#     config1 = {'conversion_target': DocumentConversionV1.NORMALIZED_TEXT}
#     text = (
#     document_conversion.convert_document(document=document1, config=config1, media_type='application/pdf').content)
#     # new_text = text.decode('utf-8').replace('\u00a0', ' ').replace('\u00ad', ' ').replace('Â', ' ').replace('    ',' ').replace('   ', ' ').replace('  ', ' ').replace('\u20b9',' ').replace('\ufffd',' ').replace('\u037e',' ').replace('\u2022',' ').replace('\u200b',' ')
#     # print text

#   return text


# def getTextViaMiner(url):
#   rsrcmgr = PDFResourceManager()
#   retstr = StringIO()
#   laparams = LAParams()
#   temptext = []
#   device = TextConverter(rsrcmgr, retstr, laparams=laparams)
#   # Open the url provided as an argument to the function and read the content
#   try:
#     f = urllib2.urlopen(urllib2.Request(url)).read()
#     # Cast to StringIO object
#     fp = StringIO(f)
#     interpreter = PDFPageInterpreter(rsrcmgr, device)
#     password = ""
#     maxpages = 0
#     caching = True
#     pagenos = set()

#     i = 0
#     for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching,
#                                   check_extractable=True):
#       interpreter.process_page(page)
#       whole = retstr.getvalue()
#       temptext.append(whole)
#       print(temptext[i])
#       i = i + 1
#       retstr.truncate(0)
#     fp.close()
#     device.close()
#   except:
#     pass
#   return " ".join(temptext)


# def getJson(url):
#   parsed = urlparse.urlparse(url)
#   docId = urlparse.parse_qs(parsed.query)['docId'][0]
#   print("Processing docId: " + docId)
#   geturl(url, config.dictPath + docId + ".pdf")

#   with open(config.dictPath+docId+'.pdf', 'rb') as document1:
#     config1 = {'conversion_target': DocumentConversionV1.NORMALIZED_TEXT}
#     text = (
#       document_conversion.convert_document(document=document1, config=config1, media_type='application/pdf').content)
#     # new_text = text.decode('utf-8').replace('\u00a0', ' ').replace('\u00ad', ' ').replace('Â', ' ').replace('    ',' ').replace('   ', ' ').replace('  ', ' ').replace('\u20b9',' ').replace('\ufffd',' ').replace('\u037e',' ').replace('\u2022',' ').replace('\u200b',' ')
#     print(text)

#   return Chunks_of_text_raw(text,url)


def Chunks_of_text(new_text):
  chunk=[]
  i = 1
  x = 0
  store = []
  chunk = 0
  prev_chunk = 0
  new_text = str(new_text, 'utf-8')
  while True:
    if len(new_text) - x < 10000:
      if x != prev_chunk:
        store.append(new_text[prev_chunk:x])
      store.append(new_text[x:])
      break
    else:
      x = new_text.find('\n', i)
      if x - prev_chunk > 6000:
        store.append(new_text[prev_chunk:x])
        prev_chunk = x
        chunk = chunk + 1
      else:
          i = x + 1
  return store


def Chunks_of_text_raw(new_text,url):
  chunk=[]
  i = 1
  x = 0
  limit = 6
  store = []
  chunk = 0
  prev_chunk = 0

  while True:
    if len(new_text) - x < 10000:
      if x != prev_chunk:
        store.append(new_text[prev_chunk:x])
      store.append(new_text[x:])
      break
    else:
      x = new_text.find('\n', i)
      if x - prev_chunk > 6000:
        store.append(new_text[prev_chunk:x])
        prev_chunk = x
        chunk = chunk + 1
      else:
          i = x + 1

  jsonRaw=watsonCallForNlu.call_to_nlu_raw(store,url)
  return jsonRaw
