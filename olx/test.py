from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get("https://www.webmotors.com.br/comprar/citroen/aircross/1-6-vti-120-flex-start-manual/4-portas/2017-2018/26933553?pos=a26933553g:&np=1")
# assert "Python" in driver.title
try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "CardSellerPhoneViewPrivate"))
    )
finally:
    element.click()
    # driver.quit()
    print (driver.find_element_by_class_name("vehicleSendProposalPrice").text)
# elem = driver.find_element_by_id("CardSellerPhoneViewPrivate")
# elem = driver.find_element_by_name("CardSeller__phone__view")
# elem.clear()
# elem.click()
# elem.send_keys(Keys.RETURN)
# assert "No results found." not in driver.page_source
# driver.close()
