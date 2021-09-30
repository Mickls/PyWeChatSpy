from pyhanlp import *


def get_result(arr):
    re_list = []
    ner = ['ns']
    for x in arr:
        temp = x.split("/")
        if (temp[1] in ner):
            re_list.append(temp[0])
    return re_list


def get_place_names(text):
    analyzer = PerceptronLexicalAnalyzer()
    segs = analyzer.analyze(text)
    arr = str(segs).split(" ")
    places = get_result(arr)
    return places
