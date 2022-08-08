import json
import re
from pprint import pprint
from tokenize import Comment

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import pandas as pd

# Setting up Virtual Chrome
from item_parser import ItemParser

googleDriverPath = "D:/Programming/ChromeDriver/chromedriver.exe"
service = Service(googleDriverPath)

url = input("Enter WowHead URL:").strip()
# url = "https://www.wowhead.com/wotlk/item=37651/the-prospectors-prize"
while url.lower() != "q":
    parser = ItemParser(service, url)
    returned_data = parser.get_item_data()

    for key in returned_data:
        print(key, ' : ', returned_data[key])

    print("Type q to quit")
    url = input("Enter WowHead URL:").strip()
