from __future__ import division
import sys
import io
import json
import string
from decimal import Decimal
import math
import operator
from collections import OrderedDict
from itertools import *
from random import shuffle
from collections import OrderedDict

def main():
	file = sys.argv[1]
	fp = open(file)
	data = fp.readlines()
	index = 0
	word_list = []
	input_line_list = OrderedDict()
	feature_count_per_line = OrderedDict()
	stop_words =   ["i", "me","my","myself","we","our","ours","ourselves","you","your","yours","yourself","yourselves","he","him","his","himself","she","her","hers","herself","it","its","itself","they","them",
"their","theirs","themselves","what","which","who","whom","this","that","these","those","am","is","are","was","were","be","been","being","have","has","had","having","do","does","did","doing","a",
"an","the","and","but","if","or","because","as","until","while","of","at","by","for","with","about","against","between","into","through","during","before","after","above","below","to","from","up","down",
"in","out","on","off","over","under","again","further","then","once","here","there","when","where","why","how","all","any","both","each","few","more","most","other","some","such","only","own","same","so","than","too","very","can","will","just","don","should","now"]
	while index < len(data):
		line_data = data[index]
		words_in_line = line_data.split()
		id = words_in_line[0]
		feature_count_per_line[id] = OrderedDict()
		input_line_list[id] = line_data
		inner_index = 3
		while inner_index < len(words_in_line):
			word_lower = words_in_line[inner_index].lower()
			exclude = set(string.punctuation)
			word = ''.join(ch for ch in word_lower if ch not in exclude)
			if word not in stop_words:
				if word not in word_list:
					word_list.append(word)
				if word not in feature_count_per_line[id]:
					feature_count_per_line[id][word] = 0
				feature_count_per_line[id][word] += 1
			inner_index += 1
		index += 1
	vanilla = {}
	vanilla["tf_wd"], vanilla["tf_b"] = perceptonTrainVanilla(word_list, input_line_list, feature_count_per_line, "True", 30)
	vanilla["pn_wd"], vanilla["pn_b"] = perceptonTrainVanilla(word_list, input_line_list, feature_count_per_line, "Pos", 30)
	average = {}
	average["tf_wd"], average["tf_b"] = perceptonTrainAverage(word_list, input_line_list, feature_count_per_line, "True", 30)
	average["pn_wd"], average["pn_b"] = perceptonTrainAverage(word_list, input_line_list, feature_count_per_line, "Pos", 30)
	with io.open('vanillamodel.txt', 'w',encoding="utf-8") as fp:
		fp.write(unicode(json.dumps(vanilla)))
	with io.open('averagedmodel.txt', 'w',encoding="utf-8") as fp:
		fp.write(unicode(json.dumps(average)))
	
def perceptonTrainVanilla(word_list, input_line_list, feature_count_per_line, className, maxIter):
	wd = {}
	for key in word_list:
		wd[key] = 0
	b = 0
	index = 0
	count = 0
	while index < maxIter:
		for key in input_line_list:
			line_data = input_line_list[key]
			words_in_line = line_data.split()
			isClass = -1
			if((words_in_line[1] == className) or (words_in_line[2] == className)):
				isClass = 1
			else:
				count += 1
			id = words_in_line[0]
			a = 0
			for word in feature_count_per_line[id]:
				a += feature_count_per_line[id][word] * wd[word]
			a = a+b
			if (isClass*a <= 0):
				for word in feature_count_per_line[id]:
					wd[word] += isClass*feature_count_per_line[id][word]
				b = b+isClass
		index += 1
	return wd,b

def perceptonTrainAverage(word_list, input_line_list, feature_count_per_line, className, maxIter):
	wd = {}
	ud = {}
	for key in word_list:
		wd[key] = 0
		ud[key] = 0
	b = 0
	B = 0
	c = 1
	index = 0
	while index < maxIter:
		for key in input_line_list:
			line_data = input_line_list[key]
			words_in_line = line_data.split()
			isClass = -1
			if((words_in_line[1] == className) or (words_in_line[2] == className)):
				isClass = 1
			id = words_in_line[0]
			a = 0
			for word in feature_count_per_line[id]:
				a += feature_count_per_line[id][word] * wd[word]
			a = a+b
			if (isClass*a <= 0):
				for word in feature_count_per_line[id]:
					wd[word] += isClass*feature_count_per_line[id][word]
					ud[word] += isClass*c*feature_count_per_line[id][word]
				b += isClass
				B += c*isClass
			c = c + 1
		index += 1
	
	for key in word_list:
		wd[key] = float(wd[key]) - (float(ud[key])/float(c))
	b = float(b) - (float(B)/float(c))
	return wd, b



if __name__ == "__main__":
    main()