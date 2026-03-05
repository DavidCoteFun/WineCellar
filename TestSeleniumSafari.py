######
# Use Selenium + Safari to:
#   - query catalog given CUP code
#   - click on product page to find its url
#   - return product url
#
# Successfully tested with Safari 26.3 on March 5th, 2026
# Completes in 5 seconds

import time
start_time = time.perf_counter()

print("Loading Safari webdriver ...")

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

cupCode='3701523800029'
beginURL="https://www.saq.com/fr/catalogsearch/result/?q=0%s&catalog_type=1"%cupCode
tmpURL2=""

from selenium.webdriver.safari.options import Options
options = Options()
#options.page_load_strategy = 'eager'
driver = webdriver.Safari(options=options)

print("[%.1f sec] Loading catalog for %s ..."%(time.perf_counter()-start_time,cupCode))
driver.get(beginURL)

#b1=driver.find_element(By.ID,"didomi-notice-agree-button")
#driver.execute_script("arguments[0].click();", b1)
#b2=driver.find_element(By.LINK_TEXT,"Voir le produit")
#driver.execute_script("arguments[0].click();", b2)

try:
    print("[%.1f sec] Accepting cookies ..."%(time.perf_counter()-start_time))
    b0 = WebDriverWait(driver,5).until(EC.visibility_of_element_located((By.ID, "didomi-notice-agree-button")))
    driver.execute_script("arguments[0].click();", b0)
    #b0.click()
except:
    pass

print("[%.1f sec] Clicking on product ..."%(time.perf_counter()-start_time))
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

print("[%.1f sec] Getting final url ..."%(time.perf_counter()-start_time))
if b1:
    nAttempts=10
    iA=0
    while iA<nAttempts:
        tmpURL2=driver.current_url
        if tmpURL2==beginURL:
            time.sleep(1)
            iA+=1
        else:
            iA=nAttempts

print(tmpURL2)
print("Total %.1f seconds"%(time.perf_counter() - start_time))

