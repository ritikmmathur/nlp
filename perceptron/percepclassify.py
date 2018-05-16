import sys
import io
import json
import string
from decimal import Decimal
import math

def main():
	fpTest = io.open(sys.argv[2],'r',  encoding="utf-8")
	outputFile = "percepoutput.txt"
	fw = io.open(outputFile, 'w', encoding="utf-8")
	data ={}
	with open(sys.argv[1]) as json_data:
		data = json.load(json_data)
	classifier = {}
	classifier["tf_wd"] = data["tf_wd"]
	classifier["pn_wd"] = data["pn_wd"]
	classifier["tf_b"] = data["tf_b"]
	classifier["pn_b"] = data["pn_b"]
	stop_words = ["i", "me","my","myself","we","our","ours","ourselves","you","your","yours","yourself","yourselves","he","him","his","himself","she","her","hers","herself","it","its","itself","they","them",
"their","theirs","themselves","what","which","who","whom","this","that","these","those","am","is","are","was","were","be","been","being","have","has","had","having","do","does","did","doing","a",
"an","the","and","but","if","or","because","as","until","while","of","at","by","for","with","about","against","between","into","through","during","before","after","above","below","to","from","up","down",
"in","out","on","off","over","under","again","further","then","once","here","there","when","where","why","how","all","any","both","each","few","more","most","other","some","such","only","own","same","so","than","too","very","can","will","just","don","should","now"]
	data = fpTest.readlines()
	index = 0
	res_string_list = []
	while index < len(data):
		word_list = data[index].split()
		a_tf = classifier["tf_b"]
		a_pn = classifier["pn_b"]
		doc_id = word_list[0]
		inner_index = 1
		feature_count = {}
		while inner_index<len(word_list):
			word_lower = word_list[inner_index].lower()
			exclude = set(string.punctuation)
			word = ''.join(ch for ch in word_lower if ch not in exclude)
			if word not in stop_words:
				if word not in feature_count:
					feature_count[word] = 0
				feature_count[word] += 1				
			inner_index += 1
		for word in feature_count:
			if word in classifier["tf_wd"]:
				a_tf += classifier["tf_wd"][word]*feature_count[word]
			if word in classifier["pn_wd"]:
				a_pn += classifier["pn_wd"][word]*feature_count[word]
		res_string = doc_id
		if(a_tf < 0):
			res_string = res_string + " " + "Fake"
		else :
			res_string = res_string + " " + "True"
		if(a_pn < 0):
			res_string = res_string + " " + "Neg"
		else :
			res_string = res_string + " " + "Pos"
		res_string += '\n'
		res_string_list.append(res_string)
		index += 1
	fw.writelines(res_string_list)




if __name__ == "__main__":
    main()
