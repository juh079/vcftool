from splinter import Browser

with Browser() as browser:
    # Visit URL
    url = "https://www.ncbi.nlm.nih.gov/snp/"
    browser.visit(url)
    browser.find_by_id('term')
    browser.fill(' q', 'q')
    # Find and click the 'search' button
    button = browser.find_by_id('search')
    # Interact with elements
    button.click()
    if browser.is_text_present('splinter.readthedocs.io'):
        print("Yes, the official website was found!")
        print(browser.text)
