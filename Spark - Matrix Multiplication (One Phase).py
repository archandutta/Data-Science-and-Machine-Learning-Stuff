from pyspark import SparkContext
import string
import sys

path_A=sys.argv[1]
path_B=sys.argv[2]
output=sys.argv[3]

sc=SparkContext(appName="Homework")
matA=sc.textFile(path_A)
matB=sc.textFile(path_B)

cellA=matA.map(lambda line:line.split(",")).map(lambda a:(int(a[1]),['A',int(a[0]),int(a[2])]))
cellB=matB.map(lambda line:line.split(",")).map(lambda b:(int(b[0]),['B',int(b[1]),int(b[2])]))


result=data=cellA.cartesian(cellB).filter(lambda c:(c[0][0]==c[1][0])).map(lambda y:((y[0][1][1],y[1][1][1]),y[0][1][2]*y[1][1][2])).reduceByKey(lambda m,n:(m+n))

save=open(output,"w")
final=result.collect()
for each in final:
	tuple=str(each[0][0])+","+str(each[0][1])+"	"+str(each[1])
	save.write(tuple)
	save.write("\n")
