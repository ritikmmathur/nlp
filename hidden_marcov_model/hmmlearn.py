import sys
import io
import json
from decimal import *


file = sys.argv[1]
fp = open(file)
data = fp.readlines()
index = 0
# {tag:count}
count_of_tag = {}
# {tag : {word : count}}
count_of_tag_with_word = {}
word_list = []
tag_list = []
count_of_tag_minus_last = {}
count_trans_from_tag1_to_tag2 = {}
while index < len(data):
	# data format word/tag
	data_line_list = data[index]
	word_tag_list_in_current_line = data_line_list.split()
	inner_index = 0
	prev_tag = "q0"
	while inner_index < len(word_tag_list_in_current_line):
		word = word_tag_list_in_current_line[inner_index].rsplit('/', 1)[0]
		tag = word_tag_list_in_current_line[inner_index].rsplit('/', 1)[1]
		# maintain word list
		if word not in word_list:
			word_list.append(word)
		# maintain tag list
		if tag not in tag_list:
			tag_list.append(tag)
		# maintain count of tags for emmission
		if tag in count_of_tag:
			count_of_tag[tag] += 1
		else:
			count_of_tag[tag] = 1

		# maintan count of tag for each word
		if tag in count_of_tag_with_word:
			if word in count_of_tag_with_word[tag]:
				count_of_tag_with_word[tag][word] += 1
			else:
				count_of_tag_with_word[tag][word] = 1
		else:
			count_of_tag_with_word[tag] = {}
			count_of_tag_with_word[tag][word] = 1

		# maintain count of tage except the last word
		if (prev_tag in count_of_tag_minus_last):
			count_of_tag_minus_last[prev_tag] += 1
		else:
			count_of_tag_minus_last[prev_tag] = 1


		# maintain transsion of tag from 1 to 2 count
		if prev_tag in count_trans_from_tag1_to_tag2:
			if tag in count_trans_from_tag1_to_tag2[prev_tag]:
				count_trans_from_tag1_to_tag2[prev_tag][tag] += 1
			else:
				count_trans_from_tag1_to_tag2[prev_tag][tag] = 1
		else:
			count_trans_from_tag1_to_tag2[prev_tag] = {}
			count_trans_from_tag1_to_tag2[prev_tag][tag] = 1
		prev_tag = tag
		inner_index += 1
	index += 1
# emission probability
index_tag_list = 0
# {tag : {word : {}}}
emission_prob_tag_associated_with_word = {}
while index_tag_list < len(tag_list):
	tag = tag_list[index_tag_list]
	emission_prob_tag_associated_with_word[tag]={}
	index_word_list = 0
	while index_word_list < len(word_list):
		word = word_list[index_word_list]
		count_word_given_tag = count_of_tag_with_word[tag][word] if (count_of_tag_with_word[tag].has_key(word)) else 0
		count_given_tag = count_of_tag[tag]
		em = count_word_given_tag/Decimal(count_given_tag)
		emission_prob_tag_associated_with_word[tag][word] = em
		index_word_list += 1
	index_tag_list += 1

index_tag_list = 0
# transion probability
initial_tag_state_list = list(tag_list)
initial_tag_state_list.append("q0")
# {tag:{toTag:{}}}
transsion_prob_tag_given_tag = {}
index_initial_tag_state_list = 0
while index_initial_tag_state_list < len(initial_tag_state_list):
	prev_tag = initial_tag_state_list[index_initial_tag_state_list]
	transsion_prob_tag_given_tag[prev_tag] = {}
	index_tag_list = 0
	vocab_size = len(tag_list)
	while index_tag_list < len(tag_list):
		cur_tag = tag_list[index_tag_list]
		# smoothing
		count_of_prev_tag_to_cur_tag = count_trans_from_tag1_to_tag2[prev_tag][cur_tag] + 1 if (count_trans_from_tag1_to_tag2.has_key(prev_tag) and count_trans_from_tag1_to_tag2[prev_tag].has_key(cur_tag)) else 1
		count_of_tag_except_last = count_of_tag_minus_last[prev_tag] + vocab_size if count_of_tag_minus_last.has_key(prev_tag) else 0
		if(count_of_tag_except_last == 0):
			ts = 0
		else:
			ts = count_of_prev_tag_to_cur_tag / Decimal(count_of_tag_except_last)
		transsion_prob_tag_given_tag[prev_tag][cur_tag] = ts
		index_tag_list += 1
	index_initial_tag_state_list += 1
learn_data = {}
learn_data["emission"] = emission_prob_tag_associated_with_word
learn_data["transsion"] = transsion_prob_tag_given_tag
json_output = json.dumps(learn_data)
with io.open('hmmmodel.txt', 'w',encoding="utf-8") as fp:
	fp.write(unicode(json_output))

