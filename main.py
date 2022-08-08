import json
import re
from pprint import pprint
from tokenize import Comment

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import pandas as pd

# Setting up Virtual Chrome
from item_filter import Filter
from item_parser import SingleItemParser
from item_parser import ItemListParser

googleDriverPath = "D:/Programming/ChromeDriver/chromedriver.exe"
service = Service(googleDriverPath)

url = input("Enter WowHead URL:").strip()
# url = "https://www.wowhead.com/wotlk/item=37651/the-prospectors-prize"
while url.lower() != "q":
    parser = ItemListParser(service, url)
    returned_data = parser.get_item_list()



    pprint(returned_data)
    print("Total Found:", len(returned_data))

    item_obj_list = []
    for k, v in returned_data.items():
        print("Searching for ", k, " ...")
        item_obj_list.append(SingleItemParser(service, v).get_item_data())

    my_filter = Filter()
    my_filter.set_ignore_armour_class(("Plate", ""))
    my_filter.set_ignore_stat(("Strength", "Agility", "Spirit"))

    item_obj_list = my_filter.filter_items(item_obj_list)

    print("Total Found after Filter:", len(item_obj_list))

    print("Type q to quit")
    url = input("Enter WowHead URL:").strip()
