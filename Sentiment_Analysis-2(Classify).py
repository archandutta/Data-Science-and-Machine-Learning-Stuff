import sys
import re
import math
#Reading parameters from the file

dataset=sys.argv[1]

vocab={}
get_param=open("nbmodel.txt","r")
priors=get_param.readline()
dec_p,tru_p,neg_p,pos_p=priors.split()
dec_p=float(dec_p)
tru_p=float(tru_p)
neg_p=float(neg_p)
pos_p=float(pos_p)

tuple=get_param.readline()
while(tuple):
	k,p1,p2,p3,p4=tuple.split()
	v=[float(p1),float(p2),float(p3),float(p4)]
	vocab[k]=v
	tuple=get_param.readline()

#Prediction

test_data=open(dataset,"r")
test_str=test_data.readline()
test_dict={}
while(test_str):
	test_review=test_str[21:]
	test_id=test_str[0:20]
	test_dict[test_id]=test_review
	test_str=test_data.readline()
#print (test_dict)

final=open("nboutput.txt","w")
for id in test_dict:
	review=test_dict[id]
	test_tokens=re.compile('\w+').findall(review)
	#number=len(test_tokens)
	prob_dec=math.log2(dec_p)
	prob_tru=math.log2(tru_p)
	prob_neg=math.log2(neg_p)
	prob_pos=math.log2(pos_p)
	for word in test_tokens:
		#print (word)
		if word in vocab:
			prob_dec=prob_dec+vocab[word][0]
			prob_tru=prob_tru+vocab[word][1]
			prob_neg=prob_neg+vocab[word][2]
			prob_pos=prob_pos+vocab[word][3]
	
	#print (prob_dec)
	#print (prob_tru)
	#print (prob_neg)
	#print (prob_pos)
	
	final.write(id)
	if prob_dec>prob_tru:
		final.write (" deceptive ")
	else:
		final.write (" truthful ")
	if prob_neg>prob_pos:
		final.write ("negative\n")
		#final.write("\n")
	else:
		final.write ("positive\n")
		#final.write("\n")
	
