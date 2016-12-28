#pip install pyvcf
import vcf
import sys


vcf_reader = vcf.Reader(open(sys.argv[1], 'r'))
for record in vcf_reader:
	print (record.ID)
	#TODO: here we would query the database
