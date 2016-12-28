#pip install pyvcf
import vcf
import sys
import requests
import json
#import urllib2
import urllib
#from BeautifulSoup import BeautifulSoup
from bs4 import BeautifulSoup
from tkinter import *
#from Tkinter import *
#from tkFileDialog import askopenfilename
#import tkMessageBox
from tkinter import messagebox
from tkinter.filedialog import askopenfilename


def main():        
        api_key = 'n-TaxdizSz6BfsVxCPxZQA'
        #Trying to make a GUI for importing the vcf file for later
        #root.title("Simple GUI")
        
        root = Tk()
        root.withdraw()
        root.update()
        root.geometry("500x500")
        root.title("Import your vcf file")
        fileName = askopenfilename(filetypes=(("VCF file","*.vcf"),("All files","*.*")))
 
        #root.mainloop()
        root.destroy()
        vcf_reader = vcf.Reader(open(fileName))
        clinvar_rsid = {}
        rsid_params = {'q': 'a' , 'fields':'clinvar.rcv.clinical_significance'}
        num_of_rsid = 0
        num_of_clinvar = 0
        num_of_uncertain = 0
        output = ''
        for record in vcf_reader:
                #rsid.append(record.ID)
                num_of_rsid+=1
                rsid_params['q'] = record.ID
                request = requests.get('http://myvariant.info/v1/query', params=rsid_params)
                request_data = request.json()
                #print(request_data)
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
                                if clinvar_rsid[record.ID] != 'Uncertain significance':
                                    num_of_uncertain = num_of_uncertain + 1
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
                                output += "******Program indicates that you might have a significant mutation! Here are some papers to check out related to this mutuation: \n"
                                journal_params = {'q': record.ID , 'fields':'grasp.publication.title'}
                                journal_request = requests.get('http://myvariant.info/v1/query', params=journal_params)
                                journal_request_data = journal_request.json()
                                for title in journal_request_data['hits'][0]['grasp']['publication']:
                                        print(title['title'])
                                        output += title['title'] + '\n'
                                print("*******************************************")
                                output += "******************************************* \n \n"
                        #print(request_data['hits'][0]['clinvar']['rcv'])
        print("number of variant genes searched: " + str(num_of_rsid) )
        output += "number of total rsid: " + str(num_of_rsid) + '\n'
        print("number of clinvar hits: " + str(num_of_clinvar) )
        output += "number of clinvar hits: " + str(num_of_clinvar) + '\n'
        print("number of benign clinical significance: " + str(num_of_uncertain))
        output += "number of benign clinical significance: " + str(num_of_uncertain) + '\n'
        if num_of_clinvar != 0:
                print("There are"+ str(num_of_uncertain*100 / num_of_clinvar) + "rsid with bengin clinical significance that with uncertain significance status")
                output += "There are "+ str(num_of_uncertain*100 / num_of_clinvar) + "%  rsid with bengin clinical significance that with uncertain significance status \n"
        #print(num_of_uncertain / num_of_clinvar * 100)
        print("we done")
        messagebox.showinfo('Result', output)
        
main()
