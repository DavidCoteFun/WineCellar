######
# Use Selenium + Chrome to:
#   - query catalog given CUP code
#   - click on product page to find its url
#   - return product url
#
# Successfully tested with Chrome 143.0.7499.170 on March 5th, 2026
# Problem: completes in 120 seconds. Very slow!

import time
start_time = time.perf_counter()

print("Loading Chrome webdriver ...")

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import threading

cupCode='3701523800029'
tmpURL2=""


from selenium.webdriver.chrome.options import Options

options = Options()
options.page_load_strategy = 'eager'
#options.add_argument("--headless=new")
#options.add_argument("--no-sandbox")

driver = webdriver.Chrome(options=options)

print("getting %s ... (%.1f sec)"%(cupCode, time.perf_counter()-start_time))
driver.get("https://www.saq.com/fr/catalogsearch/result/?q=0%s&catalog_type=1"%cupCode)

try:
    print("Accepter cookies ... (%.1f sec)"%(time.perf_counter()-start_time))
    b0 = WebDriverWait(driver,5).until(EC.visibility_of_element_located((By.ID, "didomi-notice-agree-button")))
    b0.click()
except:
    pass

print("Voir le produit ... (%.1f sec)"%(time.perf_counter()-start_time))
nAttempts=10
iA=0
while iA<nAttempts:
    try:
        b1 = WebDriverWait(driver,2).until(EC.visibility_of_element_located((By.LINK_TEXT, "Voir le produit")))
        iA=nAttempts
    except:
        iA+=1
        print("  attempt %i"%iA)

try:
    print("b1.click() ... (%.1f sec)"%(time.perf_counter()-start_time))
    driver.set_page_load_timeout(10)
    b1.click()
except:
    pass

tmpURL2=driver.current_url
print(tmpURL2)
print("Total %.1f seconds"%(time.perf_counter() - start_time))

