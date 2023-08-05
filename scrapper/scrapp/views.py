from django.shortcuts import render,HttpResponse
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .models import CollectedData
import time



def index(request):
    url = 'https://rera.punjab.gov.in/reraindex/courtview/ComplaintCaseStatusInfo'
    r = requests.get(url)
    soup = BeautifulSoup(r.content,'html.parser')
    
    tags = soup.find('a', class_ = "nav-link nav-tabs-custom-bar")['href']

    tag_url = url + tags if not tags.startswith('http') else tags
    
#   print(tags)
#   print(tag_url)

    driver = webdriver.Chrome()
    driver.get(tag_url)
    driver.maximize_window()
    
    driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/form/div/div/div/div[2]/ul/li[2]/a/span").click()
    driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/form/div/div/div/div[2]/div[1]/div[2]/div/div[1]/div/select").send_keys("Sh. Rakesh Kumar Goyal")
    driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/form/div/div/div/div[2]/div[1]/div[2]/div/div[2]/div[1]/input").send_keys("GCNo04082022") 
    driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/form/div/div/div/div[2]/div[1]/div[2]/div/div[2]/div[2]/input").clear()
    driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/form/div/div/div/div[2]/div[1]/div[2]/div/div[2]/div[2]/input").send_keys("2022")
    time.sleep(10)
    
    #captcha manual
    
    driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/form/div/div/div/div[2]/div[2]/div/input").click()
    
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.ID, 'modalOpenerButton')))

    driver.find_element(By.ID, "modalOpenerButton").click()
    time.sleep(5)
    case_data = driver.page_source

    soupp = BeautifulSoup(case_data,'html.parser')
    table_data = soupp.find_all('td')
    data_list = [td.get_text(strip=True) for td in table_data[1:]]

    for data in data_list:
        print(data)

    CollectedData.objects.create(data=data_list)

    driver.quit()
    return HttpResponse("Fetching...")
