from selenium import webdriver
from selenium.webdriver.common.by import By
import time


chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('detach', True)

driver = webdriver.Chrome(options=chrome_options)
driver.get('https://orteil.dashnet.org/experiments/cookie/')


cookie = driver.find_element(By.ID, value='cookie')


timeout = time.time() + 5
five_min = time.time() + 60*5

while True:
    cookie.click()
    if time.time() > timeout:
        right_panel = driver.find_element(By.ID, value='store')
        cookie_prices = driver.find_elements(by=By.CSS_SELECTOR, value="#store b")

        cookie_count = int(driver.find_element(By.ID, value='money').text.replace(",", ""))

        addon_dict = {}

        for n in range(len(cookie_prices)):
          if cookie_prices[n].text !='':
            addon_dict[n]= {
                'id_name':cookie_prices[n].text.split('-')[0].strip(),
                'price':int(cookie_prices[n].text.split('-')[1].strip().replace(",", ""))
            }
        max_item = None
        for item in addon_dict.values():
            
            if item['price'] <= cookie_count:
                if max_item is None or item['price'] > max_item['price']:
                    max_item = item
        if max_item is not None:
                try:
                    right_panel.find_element(By.ID, value= f'buy{max_item['id_name']}').click()
                    cookie_count -= max_item['price']
                except:
                    right_panel = driver.find_element(By.ID, value='store')
                    right_panel.find_element(By.ID, value=f'buy{max_item["id_name"]}').click()
                    cookie_count -= max_item['price']
                
        timeout = time.time() + 5
    
    if time.time() > five_min:
        cookie_per_s = driver.find_element(by=By.ID, value="cps").text
        print(cookie_per_s)
        break
          


       
