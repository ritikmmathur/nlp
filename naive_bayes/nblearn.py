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

def main():
	file = sys.argv[1]
	fp = open(file)
	data = fp.readlines()
	index = 0
	word_list = []
	word_count = 0
	true_word_count = 0
	false_word_count = 0
	neg_word_count = 0
	pos_word_count = 0
	true_words_to_count_map = {}
	false_words_to_count_map = {}
	neg_words_to_count_map = {}
	pos_words_to_count_map = {}
	word_frequency_map = {}
	while index < len(data):
		line_data = data[index]
		words_in_line = line_data.split()
		isTrueClass = False
		isPosClass = False
		if(words_in_line[1] == "True"):
			isTrueClass = True
		if(words_in_line[2] == "Pos"):
			isPosClass = True
		inner_index = 3
		while inner_index < len(words_in_line):
			word_count += 1
			word_lower = words_in_line[inner_index].lower()
			exclude = set(string.punctuation)
			word = ''.join(ch for ch in word_lower if ch not in exclude)
			if word not in word_list:
				word_list.append(word)
			if word in word_frequency_map:
				word_frequency_map[word] += 1
			else:
				word_frequency_map[word] = 1
			if (isTrueClass):
				true_word_count += 1
				if word in true_words_to_count_map:
					true_words_to_count_map[word] += 1
				else:
					true_words_to_count_map[word] = 1
			else:
				false_word_count += 1
				if word in false_words_to_count_map:
					false_words_to_count_map[word] += 1
				else:
					false_words_to_count_map[word] = 1
			if (isPosClass):
				pos_word_count += 1
				if word in pos_words_to_count_map:
					pos_words_to_count_map[word] += 1
				else:
					pos_words_to_count_map[word] = 1
			else:
				neg_word_count += 1
				if word in neg_words_to_count_map:
					neg_words_to_count_map[word] += 1
				else:
					neg_words_to_count_map[word] = 1
			inner_index += 1
		index += 1
	index = 0
	vocab = len(word_list)
	word_given_true = {}
	word_given_false = {}
	word_given_pos = {}
	word_given_neg = {}
	while index < vocab:
		word = word_list[index]
		if word in true_words_to_count_map:
			word_given_true[word] = math.log(1 + true_words_to_count_map[word]) - math.log(true_word_count + vocab)
		else:
			word_given_true[word] = math.log(1) - math.log(true_word_count + vocab)

		if word in false_words_to_count_map:
			word_given_false[word] = math.log(1 + false_words_to_count_map[word]) - math.log(false_word_count + vocab)
		else:
			word_given_false[word] = math.log(1) - math.log(false_word_count + vocab)

		if word in pos_words_to_count_map:
			word_given_pos[word] = math.log(1 + pos_words_to_count_map[word]) - math.log(pos_word_count + vocab)
		else:
			word_given_pos[word] = math.log(1) - math.log(pos_word_count + vocab)
		if word in neg_words_to_count_map:
			word_given_neg[word] = math.log(1 + neg_words_to_count_map[word]) - math.log(neg_word_count + vocab)
		else:
			word_given_neg[word] = math.log(1) - math.log(neg_word_count + vocab)
		index += 1
	sorted_x = OrderedDict(sorted(word_frequency_map.items(), key=lambda x: x[1]))
	word_to_ignore = []
	for key, value in sorted_x.items():
		if (value == 1):
			word_to_ignore.append(key)
	stop_words =  ["me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "he", "him","his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they","them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those","am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did","doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at","by", "for","with", "about", "against", "between", "into", "through", "during", "before", "after", "above","below", "to", "from","up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once","here", "there", "when", "where","why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "only", "own", "same","so", "than", "too", "very", "can", "will", "just", "should", "now"]
	for item in stop_words:
		if item not in word_to_ignore:
			word_to_ignore.append(item)
	learn_data = {}
	learn_data["true_prob"] = math.log(true_word_count/word_count)
	learn_data["false_prob"] = math.log(false_word_count/word_count)
	learn_data["pos_prob"] = math.log(pos_word_count/word_count)
	learn_data["neg_prob"] = math.log(neg_word_count/word_count)
	learn_data["word_given_neg"] = word_given_neg
	learn_data["word_given_pos"] = word_given_pos
	learn_data["word_given_false"] = word_given_false
	learn_data["word_given_true"] = word_given_true
	learn_data["word_to_ignore"] = word_to_ignore
	json_output = json.dumps(learn_data)
	with io.open('nbmodel.txt', 'w',encoding="utf-8") as fp:
		fp.write(unicode(json_output))
	

if __name__ == "__main__":
    main()