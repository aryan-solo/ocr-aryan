# -*- coding: utf-8 -*-

# we will call the NLU here
from watson_developer_cloud import NaturalLanguageUnderstandingV1
#import watson_developer_cloud.natural_language_understanding.features.v1 as Features


from watson_developer_cloud.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions

natural_language_understanding = NaturalLanguageUnderstandingV1(
    username="d4f8f1c2-741c-4af0-8dcf-b9b8106538fa",
    password="MtWIMvKCU8UY",
    version="2017-02-27")

# def call_to_nlu(list_objext):
#   final_json = []
#   l = len(list_objext)
#   for i in range(0, l):
#     response = natural_language_understanding.analyze(
#         text=str(list_objext[i]).replace('\n\n\n', " ").replace('\n\n', " ").replace('\n', " ").replace('   ',' ').replace('  ', ' '), features=[Features.Entities(emotion=False, sentiment=False, limit=250,
#                                                     model="20:fbf52bbf-9d17-4018-b978-036d6e0e1db4"),
#                                   Features.Keywords(emotion=False, sentiment=False, limit=2)])
#     final_json.append(response["entities"])
#   return final_json

def call_to_nlu(list_objext):
  final_json = []
  l = len(list_objext)
  for i in range(0, l):
    response = natural_language_understanding.analyze(
        text=str(list_objext[i]).replace('\n\n\n', " ").replace('\n\n', " ").replace('\n', " ").replace('   ',' ').replace('  ', ' '), features=Features(entities=EntitiesOptions(emotion=False, sentiment=False, limit=250,
                                                    model="20:fbf52bbf-9d17-4018-b978-036d6e0e1db4"),
                                  keywords=KeywordsOptions(emotion=False, sentiment=False, limit=2))
    )
    final_json.append(response["entities"])
  return final_json

# def call_to_nlu_raw(list_obj,url):
#     final_json = []
#     l = len(list_obj)
#     for i in range(0, l):
#         response = natural_language_understanding.analyze(
#             text=str(list_obj[i]).replace('\n\n\n', " ").replace('\n\n', " ").replace('\n', " ").replace('   ',
#                                                                                                             ' ').replace(
#                 '  ', ' '), features=[Features.Entities(emotion=False, sentiment=False, limit=250,
#                                                         model="20:2a815510-85a4-4ffd-a470-043707eb1b33"),
#                                       Features.Keywords(emotion=False, sentiment=False, limit=2)])
#         final_json.append(response["entities"])
#     return final_json

def call_to_nlu_raw(list_obj,url):
    final_json = []
    l = len(list_obj)
    for i in range(0, l):
        response = natural_language_understanding.analyze(
            text=str(list_obj[i]).replace('\n\n\n', " ").replace('\n\n', " ").replace('\n', " ").replace('   ',
                                                                                                            ' ').replace(
                '  ', ' '), features=Features(entities=EntitiesOptions(emotion=False, sentiment=False, limit=250,
                                                        model="20:2a815510-85a4-4ffd-a470-043707eb1b33"),
                                      keywords=KeywordsOptions(emotion=False, sentiment=False, limit=2))
        )
        final_json.append(response["entities"])
    return final_json



# def getJsonFromWatson(textPath):
#     final_json = []
#     with open(textPath, 'rb') as t:
#         content = t.read()
#     content = str(content)[2:-1]
#     response = natural_language_understanding.analyze(text=content.replace('   ', ' ').replace('  ',' '),
#         features=[Features.Entities(emotion=False,sentiment=False,limit=250,model = '20:fbf52bbf-9d17-4018-b978-036d6e0e1db4'),
#         Features.Keywords(emotion=False,sentiment=False,limit=2)])
#     final_json.append(response["entities"])
#     return final_json

def getJsonFromWatson(textPath):
    final_json = []
    with open(textPath, 'rb') as t:
        content = t.read()
    content = str(content)[2:-1]
    response = natural_language_understanding.analyze(text=content.replace('   ', ' ').replace('  ',' '),
        features=Features(entities=EntitiesOptions(emotion=False,sentiment=False,limit=250,model = '20:fbf52bbf-9d17-4018-b978-036d6e0e1db4'),
        keywords=KeywordsOptions(emotion=False,sentiment=False,limit=2))
                                                      )
    final_json.append(response["entities"])
    return final_json