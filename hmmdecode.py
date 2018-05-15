import sys
import io
import json
from decimal import *

def get_max_val_for_veterbi(veterbi, states, t, cur_tag, word, emission, transsion):
	tag = states[0]
	em = emission[cur_tag][word] if emission.has_key(cur_tag) and emission[cur_tag].has_key(word) else 1
	ts = transsion[tag][cur_tag] if transsion.has_key(tag) and transsion[tag].has_key(cur_tag) else 0
	index = t
	val = veterbi[index][tag]*em*ts
	val2 = veterbi[index][tag]*ts
	max_tag = tag
	index1 = 1
	while index1 < len(states):
		tag = states[index1]
		em = emission[cur_tag][word] if emission.has_key(cur_tag) and emission[cur_tag].has_key(word) else 1
		ts = transsion[tag][cur_tag] if transsion.has_key(tag) and transsion[tag].has_key(cur_tag) else 0
		tmp = veterbi[index][tag]*em*ts
		tmp2 = veterbi[index][tag]*ts
		if(tmp > val): 
			val = tmp
		if(tmp2 > val2):
			val2 = tmp2
			max_tag = tag
		index1 += 1
	res = {}
	res["val"] = val
	res["tag"] = max_tag
	return res

file = sys.argv[1]
fp = io.open(file,'r',  encoding="utf-8")
outputFile = "hmmoutput.txt"
fw = io.open(outputFile, 'w', encoding="utf-8")

d ={}
with open('hmmmodel.txt') as json_data:
    d = json.load(json_data)
# decoding
# {tag:{toTag:{}}}
transsion_prob_tag_given_tag = d["transsion"]
# {tag : {word : {}}}
emission_prob_tag_associated_with_word = d["emission"]
state_tag_list = transsion_prob_tag_given_tag.keys()
state_tag_list.remove("q0")
data = fp.readlines()
data_line_list = []
index = 0
res_string_list = []
while index < len(data):
	data_line_list.append(data[index])
	word_tag_list_in_current_line = data_line_list[index].split()
	word = word_tag_list_in_current_line[0]
	#inistialize
	# row represent states and column words
	veterbi = [{}]
	backtrack = [{}]
	for tag in state_tag_list:
		em = emission_prob_tag_associated_with_word[tag][word] if emission_prob_tag_associated_with_word.has_key(tag) and emission_prob_tag_associated_with_word[tag].has_key(word) else 1
		ts = transsion_prob_tag_given_tag["q0"][tag] if transsion_prob_tag_given_tag.has_key("q0") and transsion_prob_tag_given_tag["q0"].has_key(tag) else 0
		veterbi[0][tag] = em*ts
		backtrack[0][tag] = "q0"
	# first word already considered
	inner_index = 1
	while inner_index < len(word_tag_list_in_current_line):
		# adding new row
		veterbi.append({})
		backtrack.append({})
		index1 = 0
		maximum = 0
		word = word_tag_list_in_current_line[inner_index]
		while index1 < len(state_tag_list):
			cur_tag = state_tag_list[index1]
			t = inner_index-1
			res = get_max_val_for_veterbi(veterbi, state_tag_list, t, cur_tag, word, emission_prob_tag_associated_with_word, transsion_prob_tag_given_tag)
			veterbi[inner_index][cur_tag] = res["val"]
			backtrack[inner_index][cur_tag] = res["tag"]
			index1 += 1
		inner_index += 1
	last = inner_index -1
	index1 = 1
	tag = state_tag_list[0]
	max_value = veterbi[last][tag]
	max_tag = tag
	while index1<len(state_tag_list):
		tag = state_tag_list[index1]
		if(veterbi[last][tag]>max_value):
			max_value = veterbi[last][tag]
			max_tag = tag
		index1 += 1
	ans_tag = []
	ans_tag.append(max_tag)
	while last>0:
		max_tag = backtrack[last][max_tag]
		ans_tag.append(max_tag)
		last -= 1
	index += 1
	ans_tag.reverse()
	index1 = 1
	res_string = word_tag_list_in_current_line[0] + '/' + ans_tag[0]
	while index1<len(ans_tag):
		res_string = res_string + " " + word_tag_list_in_current_line[index1] + '/' +ans_tag[index1]
		index1 += 1
	res_string += '\n'
	res_string_list.append(res_string)
fw.writelines(res_string_list)













