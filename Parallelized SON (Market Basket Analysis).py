from pyspark import SparkContext
sc=SparkContext(appName="HW2")

import itertools
import sys

input_File=sys.argv[1]
value=sys.argv[2]
min_Support=float(value)
output_File=sys.argv[3]

def sep(x):
	return x.split(",")

def convert(array):
	list=[]
	for n in array:
		list.append(int(n))
	return list

def APRIORI_Phase_one_Map(array):
	b=[]
	num_bask=0
	l=0
	max=0
	for x in array:
		b.append(x)
		num_bask=num_bask+1
		l=len(x)
		if(max<l):
			max=l
	support_count=min_Support*num_bask
	dict={}
	for i in range(1,max+1):
		res=[]
		for x in b:
			res=[]
			res.extend(itertools.combinations(x,i))
			for n in res:
				if i==1:
					key=n
					if key in dict:
						dict[key]=dict[key]+1
					else:
						dict[key]=1
				else:
					flag=0
					key=n
					temp=[]
					temp.extend(itertools.combinations(key,i-1))
					for a in temp:
						if a not in dict:
							flag=1
					if flag==0:
						if key in dict:
							dict[key]=dict[key]+1
						else:
							dict[key]=1
	for key in dict.keys():
		if dict[key]<support_count:
			del dict[key]
	local_freq=[]
	for key in dict:
		local_freq.append((key,1))
	print local_freq
	return local_freq
	
def Phase_two_Map(array):
	global cand_items
	b=[]
	num_bask=0
	l=0
	max=0
	for x in array:
		b.append(x)
		num_bask=num_bask+1
		l=len(x)
		if(max<l):
			max=l
	dict={}
	for i in range(1,max+1):
		res=[]
		for x in b:
			res=[]
			res.extend(itertools.combinations(x,i))
			for n in res:
					key=n
					if key in dict:
						dict[key]=dict[key]+1
					else:
						dict[key]=1
	freq_count=[]
	for item in cand_items:
		if item[0] in dict:
			freq_count.append((item[0],dict[item[0]]))
	return freq_count

def Global_freq(x,y):
	global total_bask
	global min_Support
	support_count=min_Support*total_bask
	#print x 
	#print y
	if (x+y)>=support_count:
		return (x+y)

values=sc.textFile(input_File)
lines=values.map(sep)
basket=lines.map(convert)
all_baskets=basket.collect()
total_bask=0
for b in all_baskets:
	total_bask=total_bask+1
	
map_one=basket.mapPartitions(APRIORI_Phase_one_Map)
reduce_one=map_one.reduceByKey(lambda x,y:x)
cand_items=reduce_one.collect()
map_two=basket.mapPartitions(Phase_two_Map)
reduce_two=map_two.reduceByKey(Global_freq)
final_items=reduce_two.collect()
support_count=min_Support*total_bask

save=open(output_File,"w")
for each in final_items:
	tuple=""
	if(each[1]>=support_count):
		for element in each[0]:
			tuple=tuple+str(element)+","
		tuple=tuple[:-1]
		save.write(tuple)
		save.write("\n")