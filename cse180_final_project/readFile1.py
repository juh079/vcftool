#pip install pyvcf
import vcf
import sys
import requests
import json
#import urllib2
import urllib
#from BeautifulSoup import BeautifulSoup
from bs4 import BeautifulSoup
#from Tkinter import *
from tkinter import *
#from tkFileDialog import askopenfilename
from tkinter.filedialog import askopenfilename

#import plotly 
#import plotly.plotly as py
#import plotly.graph_objs as go
#plotly.tools.set_credentials_file(username='cse180team', api_key='KNHRMV4kJexfbIGL568X')

def main():        
        api_key = 'n-TaxdizSz6BfsVxCPxZQA'
        #Trying to make a GUI for importing the vcf file for later
        #root.title("Simple GUI")
        #root.geometry("500x500")
        root = Tk()
        root.withdraw()
        root.update()
        fileName = askopenfilename(filetypes=(("VCF file","*.vcf"),("All files","*.*")))

#        print (fileName)
#        with open(fileName) as f:
#                print(f.readlines())
#        f.close()
 
        #root.mainloop()
        root.destroy()
        vcf_reader = vcf.Reader(open(fileName))
        clinvar_rsid = {}
        rsid_params = {'q': 'a' , 'fields':'clinvar.rcv.clinical_significance'}
        num_of_rsid = 0
        num_of_clinvar = 0
        for record in vcf_reader:
                #rsid.append(record.ID)
                num_of_rsid+=1
                rsid_params['q'] = record.ID
                request = requests.get('http://myvariant.info/v1/query', params=rsid_params)
                request_data = request.json()
                #print(request_data)
                #print("testing " + record.ID)
                if 'hits' not in request_data:
                        continue
                elif len(request_data['hits']) == 0:
                        continue
                elif 'clinvar' not in request_data['hits'][0]:
                        continue
                elif 'rcv' not in request_data['hits'][0]['clinvar']:
                        continue
                elif type(request_data['hits'][0]['clinvar']['rcv']) is dict:
                #elif len(request_data['hits'][0]['clinvar']['rcv']) == 0
                        if 'clinical_significance' not in request_data['hits'][0]['clinvar']['rcv']:
                                continue
                        else:
                                clinvar_rsid[record.ID] = request_data['hits'][0]['clinvar']['rcv']['clinical_significance']
                                num_of_clinvar+=1
                                print(record.ID + " : " + record.REF + " to " + str(record.ALT[0]) + " mutation at chromosome " + record.CHROM + ", clinical_significance is: " + clinvar_rsid[record.ID])
                                #print(request_data['hits'][0]['clinvar']['rcv'])
                elif type(request_data['hits'][0]['clinvar']['rcv']) is list:
                        #print("testing " + record.ID)
                        check = False
                        if len(request_data['hits'][0]['clinvar']['rcv']) == 0:
                                continue
                        for i in request_data['hits'][0]['clinvar']['rcv']:
                                if 'clinical_significance' not in i:
                                        continue
                                else:
                                        check = True
                                        clinvar_rsid[record.ID] = i['clinical_significance'] 
                                        num_of_clinvar+=1
                                        print(record.ID + " : " + record.REF + " to " + str(record.ALT[0]) + " mutation at chromosome " + record.CHROM + ", clinical_significance is: " + clinvar_rsid[record.ID])
                        if check==True:
                                print("******Program indicates that you might have a significant mutation! Here are some papers to check out related to this mutuation:")
                                journal_params = {'q': record.ID , 'fields':'grasp.publication.title'}
                                journal_request = requests.get('http://myvariant.info/v1/query', params=journal_params)
                                journal_request_data = journal_request.json()
                                for title in journal_request_data['hits'][0]['grasp']['publication']:
                                        print(title['title'])
                                print("*******************************************")
        

        print("number of total rsid: " + str(num_of_rsid) )
        print("number of clinvar hits: " + str(num_of_clinvar) )
        print("we done")
        
#        labels = ['total', 'clinvar hits']
#        values = [num_of_rsid, num_of_clinvar]
#        trace=go.Pie(labels=labels,values=values)
#        py.iplot([trace])

        #print(rsid)
        #print("*****************************************************")
	#TODO: here we would query the database
        #response = requests.get('https://www.ncbi.nlm.nih.gov/projects/SNP/snp_ref.cgi?searchType=adhoc_search&type=rs&rs=rs2462492') 

        #request = requests.get('http://myvariant.info/v1/query?q=rs4746&fields=clinvar.rcv.clinical_significance')
#        request = requests.get('http://myvariant.info/v1/query', params=rsid_params)
#        request_data = request.json()
#        print(request_data)
#        if 'hits' not in request_data:
#                print ("no values")
#        elif 'clinvar' not in request_data['hits'][0]:
#                print ("no values")
#        elif 'rcv' not in request_data['hits'][0]['clinvar']:
#                print ("no values")
#        else:
#                print(request_data['hits'][0]['clinvar']['rcv'])
 
        #print(request.text)
        #print(response.text)
        #xml_string = response.text
        
#        soup = BeautifulSoup(xml_string)
#        print soup.find('preferredTitle')
        
main()
