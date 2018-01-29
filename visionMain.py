import sys
sys.path.insert(0, '/home/pankaj/ocr/lib/services')
import visionApi
import removeJunk as RJ
import asyncio

loop = asyncio.get_event_loop()
def getTextForBatch(list):
		res = visionApi.getresponseImage(list)
		res_list = res.responses
		text_str = ''
		for obj in res_list:
			text = RJ.removeJunk(obj, True)
			text_str = text+' '+text_str
		return text_str

def getTextForImage(Arr,textpath):
		Arr.reverse()
		final = []
		for n in range(0,len(Arr),16):
			try:
				new_A = Arr[n:n+16]
			except:
				new_A = Arr[n:]
			final.append(new_A)
		futures = [asyncio.ensure_future(callAsync(i), loop=loop) for i in final]
		full_response_list = loop.run_until_complete(asyncio.gather(*futures))
		full_response_list.reverse()
		text_str_b = ' '.join(full_response_list)
		word_list = text_str_b.split()
		text_str_f = ' '.join(word_list)
		with open(textpath, 'w',encoding='utf-8') as a:
			a.write(text_str_f)
		return text_str_f

async def callAsync(args):
	response = await loop.run_in_executor(None, getTextForBatch, args)
	return response