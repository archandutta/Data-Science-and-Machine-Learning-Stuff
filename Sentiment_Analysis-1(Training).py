import re
import math
import sys
import string

dataset=sys.argv[1]
dataset_label=sys.argv[2]

#Get data into proper form

stop_words=["chicago","hotel","husband","wife","a", "about", "above", "above", "across", "after", "afterwards", "again", "against", "all", "almost", "alone", "along", "already", "also","although","always","am","among", "amongst", "amoungst", "amount",  "an", "and", "another", "any","anyhow","anyone","anything","anyway", "anywhere", "are", "around", "as",  "at", "back","be","became", "because","become","becomes", "becoming", "been", "before", "beforehand", "behind", "being", "below", "beside", "besides", "between", "beyond", "bill", "both", "bottom","but", "by", "call", "can", "cannot", "cant", "co", "con", "could", "couldnt", "cry", "de", "describe", "detail", "do", "done", "down", "due", "during", "each", "eg", "eight", "either", "eleven","else", "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere", "except", "few", "fifteen", "fify", "fill", "find", "fire", "first", "five", "for", "former", "formerly", "forty", "found", "four", "from", "front", "full", "further", "get", "give", "go", "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his", "how", "however", "hundred", "ie", "if", "in", "inc", "indeed", "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter", "latterly", "least", "less", "ltd", "made", "many", "may", "me", "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly", "move", "much", "must", "my", "myself", "name", "namely", "neither", "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone", "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on", "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out", "over", "own","part", "per", "perhaps", "please", "put", "rather", "re", "same", "see", "seem", "seemed", "seeming", "seems", "serious", "several", "she", "should", "show", "side", "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", "such", "system", "take", "ten", "than", "that", "the", "their", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "therefore", "therein", "thereupon", "these", "they", "thickv", "thin", "third", "this", "those", "though", "three", "through", "throughout", "thru", "thus", "to", "together", "too", "top", "toward", "towards", "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us", "very", "via", "was", "we", "well", "were", "what", "whatever", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which", "while", "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", "with", "within", "without", "would", "yet", "you", "your", "yours", "yourself", "yourselves", "the"];

dec_count=0
tru_count=0
neg_count=0
pos_count=0
total_count=0
dict={}

data=open(dataset,"r")
labels=open(dataset_label,"r")
row=data.readline()
while(row):
	review=row[21:]
	string=labels.readline()
	key, class1, class2 =string.split()
	total_count=total_count+1
	if class1=="deceptive":
		dec_count=dec_count+1	
	else:
		tru_count=tru_count+1	
	if class2=="negative":
		neg_count=neg_count+1	
	else:
		pos_count=pos_count+1	
	#print (class1)
	#print (class2)
	obs=[review,class1,class2]
	dict[key]=obs
	row=data.readline()
#print (dict)


#print(total_count)
#print(dec_count)
#print(tru_count)
#print(neg_count)
#print(pos_count)

dec_p=dec_count/total_count
tru_p=tru_count/total_count
neg_p=neg_count/total_count
pos_p=pos_count/total_count

#Tokenizer
vocab={}
token_list=[]

for key in dict:
	review=dict[key][0]
	class1=dict[key][1]
	class2=dict[key][2]
	token_list=re.compile('\w+').findall(review)
	#print (token_list)
	number=len(token_list)
	j=0
	while(j<number):
		token=token_list[j]
		token=token.lower()
		if token in stop_words:
			j=j+1
			continue
		if token not in vocab:
			if class1=="deceptive":
				vocab[token]=[1,0,0,0]
			else:
				vocab[token]=[0,1,0,0]
			if class2=="negative":
				vocab[token][2]=1
			else:
				vocab[token][3]=1
		else:
			if class1=="deceptive":
				vocab[token][0]=vocab[token][0]+1
			else:
				vocab[token][1]=vocab[token][1]+1
			if class2=="negative":
				vocab[token][2]=vocab[token][2]+1
			else:
				vocab[token][3]=vocab[token][3]+1
				   	
		j=j+1

#print (len(vocab))
#print (vocab)

#Calculate Probabilities and Laplace Smoothing

v_len=len(vocab)
dec_freq=0
tru_freq=0
neg_freq=0
pos_freq=0

for each in vocab:
	dec_freq=dec_freq+vocab[each][0]
	tru_freq=tru_freq+vocab[each][1]
	neg_freq=neg_freq+vocab[each][2]
	pos_freq=pos_freq+vocab[each][3]

#print(dec_freq)
#print(tru_freq)
#print(neg_freq)
#print(pos_freq)

for w in vocab:
	vocab[w][0]=math.log2(vocab[w][0]+1)-math.log2(dec_freq+v_len)
	vocab[w][1]=math.log2(vocab[w][1]+1)-math.log2(tru_freq+v_len)
	vocab[w][2]=math.log2(vocab[w][2]+1)-math.log2(neg_freq+v_len)
	vocab[w][3]=math.log2(vocab[w][3]+1)-math.log2(pos_freq+v_len)

#print(len(vocab))
#print(vocab)
		
#Saving parameters in a file

save=open("nbmodel.txt","w")
priors=str(dec_p)+" "+str(tru_p)+" "+str(neg_p)+" "+str(pos_p)
save.write(priors)
save.write("\n")
for k,v in vocab.items():
	#print (k,v)
	p1,p2,p3,p4=v
	tuple=k+" "+str(p1)+" "+str(p2)+" "+str(p3)+" "+str(p4)
	save.write(tuple)
	save.write("\n")
