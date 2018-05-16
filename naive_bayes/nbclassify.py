import sys
import io
import json
import string
from decimal import Decimal
import math

def main():
	file = sys.argv[1]
	fp = io.open(file,'r',  encoding="utf-8")
	outputFile = "nboutput.txt"
	fw = io.open(outputFile, 'w', encoding="utf-8")
	data ={}
	with open('nbmodel.txt') as json_data:
		data = json.load(json_data)
	word_given_true = data["word_given_true"]
	word_given_false = data["word_given_false"]
	word_given_pos = data["word_given_pos"]
	word_given_neg = data["word_given_neg"]
	true_prob = data["true_prob"]
	false_prob = data["false_prob"]
	pos_prob = data["pos_prob"]
	neg_prob = data["neg_prob"]
	word_to_ignore = data["word_to_ignore"]
	
	data = fp.readlines()
	index = 0
	res_string_list = []
	while index < len(data):
		word_list = data[index].split()
		prob_true_class = true_prob
		prob_false_class = false_prob
		prob_neg_class = neg_prob
		prob_pos_class = pos_prob
		doc_id = word_list[0]
		inner_index = 1
		while inner_index<len(word_list):
			word_lower = word_list[inner_index].lower()
			exclude = set(string.punctuation)
			word = ''.join(ch for ch in word_lower if ch not in exclude)
			if word not in word_to_ignore:
				if word in word_given_true:
					prob_true_class = prob_true_class + word_given_true[word]
				if word in word_given_false:
					prob_false_class = prob_false_class + word_given_false[word]
				if word in word_given_pos:
					prob_pos_class = prob_pos_class + word_given_pos[word]
				if word in word_given_neg:
					prob_neg_class = prob_neg_class + word_given_neg[word]
			inner_index += 1
		res_string = doc_id
		if(prob_true_class > prob_false_class):
			res_string = res_string + " " + "True"
		else :
			res_string = res_string + " " + "Fake"
		if(prob_pos_class > prob_neg_class):
			res_string = res_string + " " + "Pos"
		else :
			res_string = res_string + " " + "Neg"
		res_string += '\n'
		res_string_list.append(res_string)
		index += 1
	fw.writelines(res_string_list)




if __name__ == "__main__":
    main()
