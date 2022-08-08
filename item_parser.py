import json
import re
from pprint import pprint
from tokenize import Comment

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import pandas as pd


class ItemParser:
    item_property_names = (
        "Stamina",
        "Intellect",
        "Hit",
        "Haste",
        "Critical Strike",
        "Spell Power"
    )

    def __init__(self, service, url):
        self.url = url
        browser = webdriver.Chrome(service=service)
        browser.get(url)
        content = browser.page_source

        self.soup_content = BeautifulSoup(content, "html.parser")
        self.tooltip = self.soup_content.find("div", attrs={'class': 'wowhead-tooltip'})
        # Closing Virtual Chrome browser after we are done
        browser.quit()

    def get_item_data(self):
        tooltip = self.tooltip

        item_data = {
            "Type": self.get_item_type(),
            "Armour Class": self.get_armour_class(),
            "Name": self.get_item_name(),
            "Item Level": self.get_item_level()}
        item_data.update(self.get_core_stats())
        item_data.update(self.get_secondary_stats())

        return item_data

    def get_item_name(self):
        return self.tooltip.find("b").text

    def get_core_stats(self):
        spans = self.tooltip.find_all("span")
        core_stat_list = {}
        for s in spans:
            sting = s.text
            if len(sting) == 0:
                continue

            # Spans with + have main stats in them
            if sting[0] == "+":
                key_name = sting.split(" ")[1]
                core_stat_list[key_name] = re.search(r'\d+', sting).group()
                continue

        return core_stat_list

    def get_secondary_stats(self):
        spans = self.tooltip.find_all("span", attrs={"class": "q2"})
        secondary_stat_list = {}
        for s in spans:
            s = s.text

            for property_name in ItemParser.item_property_names:
                if re.search(property_name, s, re.IGNORECASE):
                    secondary_stat_list[property_name] = re.search(r'\d+', s).group()

        return secondary_stat_list

    def get_item_level(self):
        spans = self.tooltip.find_all("span")
        return re.search(r'\d+', spans[0].text).group()

    def get_item_type(self):
        td = self.tooltip.find_all("td")
        return td[2].text

    def get_armour_class(self):
        span = self.tooltip.find("span", "q1")
        return span.text if span.text else "None"