from splinter import Browser
import vcf
import sys
from time import sleep

with Browser() as browser:
    # Visit URL
    url = "https://www.ncbi.nlm.nih.gov/snp/"
    browser.visit(url)
    # Find and click the 'search' button
    #button = browser.find_by_id("search")

    vcf_reader = vcf.Reader(open(sys.argv[1], 'r'))

    for record in vcf_reader:
        browser.fill('term', record.ID)
        button = browser.find_by_id("search")
        button.click()
        sleep(1)

#    if browser.is_text_present('rs7418179'):
#        print("Yes, the official website was found!")
#    else:
#        print("No, it wasn't found... We need to improve our SEO techniques")

