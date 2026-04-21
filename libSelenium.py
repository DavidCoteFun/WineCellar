"""
Created on March 5th, 2026
@author: dcote

See TestSeleniumSafari.py for details
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def getProductURL(cupCode):
    print("getProductURL for CUP %s"%cupCode)
    beginURL="https://www.saq.com/fr/catalogsearch/result/?q=0%s&catalog_type=1"%cupCode
    productURL=None

    from selenium.webdriver.safari.options import Options
    options = Options()
    #options.page_load_strategy = 'eager'
    driver = webdriver.Safari(options=options)

    driver.get(beginURL)
    try:
        b0 = WebDriverWait(driver,5).until(EC.visibility_of_element_located((By.ID, "didomi-notice-agree-button")))
        driver.execute_script("arguments[0].click();", b0)
        #b0.click()
    except:
        pass

    nAttempts=10
    iA=0
    b1=None
    while iA<nAttempts:
        try:
            b1 = WebDriverWait(driver,2).until(EC.visibility_of_element_located((By.LINK_TEXT, "Voir le produit")))
            driver.execute_script("arguments[0].click();", b1)
            #b1.click()
            iA=nAttempts
        except:
            iA+=1
            print("  attempt %i"%iA)

    if b1:
        nAttempts=10
        iA=0
        while iA<nAttempts:
            productURL=driver.current_url
            if productURL==beginURL:
                time.sleep(1)
                iA+=1
            else:
                iA=nAttempts

    print("getProductURL %s"%productURL)
    return productURL

