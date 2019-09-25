# -*- coding: utf-8 -*-
__author__      = "Tao Zhu"
import re
import argparse

parser = argparse.ArgumentParser()
parser = argparse.ArgumentParser(description = 'Extract fasta sequence')
parser.add_argument('-o','--output',help="The output file",type=str,required=True)
parser.add_argument('-i','--input',help="The input file",type=str,required=True)

args = parser.parse_args()

def fastawrit(list,listname,file):
	f=open(file,"a+")
	a=0
	f.write(">"+str(listname)+"\n")
	while a < len(list):
		cache=list[a:(a+80)]
		a+=80
		f.write(cache+'\n')
	f.close()

def vcf(filepath):
	vcffile=open(filepath,"r")
	sample=[]
	result={}
	for line in vcffile:
		ref=[]
		alt=[]
		genetype=[]
		if line.startswith("#CHROM"):
			sample=line.strip("\n").split("\t")[9:]
			for i in sample:
				result[i]=""
		elif line.startswith("##"):
			pass
		else:
			realgenetype=[]
			genetype_dict={}
			genetype=re.findall("(?<=/|\|).",line)
			ref=line.split("\t")[3]
			alt=line.split("\t")[4].split(",")
			for i in genetype:
				if i == ".":
					realgenetype.append("N")
				elif int(i) == 0:
					realgenetype.append(ref[0])
				else:
					realgenetype.append(alt[int(i)-1])
			for i in range(0,len(sample)):
				genetype_dict[sample[i]]=realgenetype[i]
				pass
			for j in genetype_dict:
				result[j]=result[j]+genetype_dict[j]
				pass
	return (result)
if __name__ == '__main__':
	if args.output and args.input != None :
		fa=vcf(args.input)
		for i in fa:
			fastawrit(fa[i],i,args.output)