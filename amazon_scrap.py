import os
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv

class Amazon():

    def __init__(self):

        # Here i get path of current workind directory
        self.current_path = os.getcwd()
        self.url = 'https://www.amazon.com'
        # Chromedriver is just like a chrome. you can dowload latest by it website
        self.driver_path = os.path.join(os.getcwd(), 'chromedriver.exe')
        self.driver = webdriver.Chrome(self.driver_path)

    def page_load(self):

        self.driver.get(self.url)
        # Here I get search field id from driver
        print("inside page_load")
        search_field = self.driver.find_element_by_id('twotabsearchtextbox')
        # Here .send_keys is use to input text in search field
        search_field.send_keys('smartphone' + '\n')
        # Here time.sleep is used to add delay for loading context in browser
        time.sleep(3)
        phones_upto_50 = self.driver.find_element_by_link_text('Up to $50')
        phones_upto_50.click()
        time.sleep(5)
        # Here we fetched driver page source from driver.
        page_html = self.driver.page_source
        # Here BeautifulSoup is dump page source into html format
        self.soup = BeautifulSoup(page_html, 'html.parser')
        # print(self.soup.prettify)

    def create_csv_file(self):
        print("inside create csv")
        # Here I created CSV file with desired header.
        rowHeaders = ["Name", "Price in Rupees"]
        self.file_csv = open('Amazon_output.csv', 'w', newline='', encoding='utf-8')
        self.mycsv = csv.DictWriter(self.file_csv, fieldnames=rowHeaders)
        # Writeheader is pre-defined function to write header
        self.mycsv.writeheader()

    def data_scrap(self):

        print("inside data scrap")
        # Here I fetch all products div elements
        first_page_mobiles_names = (self.soup.find_all('span', class_='a-size-medium a-color-base a-text-normal'))
        first_page_mobiles_price = (self.soup.find_all('span', class_='a-offscreen'))
        for j,k in zip(first_page_mobiles_names,first_page_mobiles_price):
            self.mycsv.writerow({"Name": j.text, "Price in Rupees": k.text})

    def tearDown(self):
        print("inside tear down")
        # Here driver.quit function is used to close chromedriver
        self.driver.quit()
        # Here we also need to close Csv file which I generated above
        self.file_csv.close()

if __name__ == "__main__":

    Amazon = Amazon()
    Amazon.page_load()
    Amazon.create_csv_file()
    Amazon.data_scrap()
    Amazon.tearDown()
    print("Task completed")