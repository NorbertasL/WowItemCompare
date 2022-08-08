import json
import re
import time
from pprint import pprint
from tokenize import Comment

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from item_obj import Item
import pandas as pd


class SingleItemParser:
    item_property_names = (  # This is only used for secondary stats
        "Strength",
        "Stamina",
        "Agility",
        "Intellect",
        "Spirit",
        "Mana Per 5",
        "Hit",
        "Haste",
        "Critical Strike",
        "Expertise",
        "Spell Power",
        "Spell Damage",
        "Healing Healing"
    )

    def __init__(self, service, url):
        self.url = url

        browser = _get_chrom_driver(service)
        browser.get(url)
        content = browser.page_source

        self.soup_content = BeautifulSoup(content, "html.parser")
        self.tooltip = self.soup_content.find("div", attrs={'class': 'wowhead-tooltip'})
        # Closing Virtual Chrome browser after we are done
        browser.quit()

    def get_item_data(self):
        tooltip = self.tooltip

        item_object = Item(self.get_item_name())
        item_object.set_parameter(Item.PARAMETERS.TYPE, self.get_item_type())
        item_object.set_parameter(Item.PARAMETERS.ARMOUR_CLASS, self.get_armour_class())
        item_object.set_parameter(Item.PARAMETERS.CORE_STATS, self.get_core_stats())
        item_object.set_parameter(Item.PARAMETERS.SOCKETS, self.get_sockets())

        secondary_stat_list, proc_effect_list, user_effect_list, unknown_effect_list = self.get_secondary_stats()

        item_object.set_parameter(Item.PARAMETERS.SECONDARY_STATS, secondary_stat_list)
        item_object.set_parameter(Item.PARAMETERS.PROC_EFFECT, proc_effect_list)
        item_object.set_parameter(Item.PARAMETERS.USE_EFFECTS, user_effect_list)
        item_object.set_parameter(Item.PARAMETERS.OTHER, unknown_effect_list)

        return item_object
        """
        item_data = {
            "Type": self.get_item_type(),
            "Armour Class": self.get_armour_class(),
            "Name": self.get_item_name(),
            "Item Level": self.get_item_level()}
        item_data.update(self.get_core_stats())
        item_data.update(self.get_sockets())
        item_data.update(self.get_socket_bonus())
        item_data.update(self.get_secondary_stats())

        return item_data
        """

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
        proc_effect_list = {}
        user_effect_list = {}
        unknown_effect_list = {}
        for s in spans:
            s = s.text

            if s.startswith("Use:"):
                user_effect_list[Item.PARAMETERS.USE_EFFECTS.name] = s

            else:
                if "proc" in s.lower():
                    # Has a proc in string so a proc effect
                    proc_effect_list[Item.PARAMETERS.PROC_EFFECT.name] = s
                else:
                    for property_name in SingleItemParser.item_property_names:
                        if re.search(property_name, s, re.IGNORECASE):
                            secondary_stat_list[property_name] = re.search(r'\d+', s).group()
                            continue
                    unknown_effect_list[Item.PARAMETERS.OTHER.name] = s

        return secondary_stat_list, proc_effect_list, user_effect_list, unknown_effect_list

    def get_item_level(self):
        spans = self.tooltip.find_all("span")
        return re.search(r'\d+', spans[0].text).group()

    def get_item_type(self):
        td = self.tooltip.find_all("td")
        return td[2].text

    def get_armour_class(self):
        span = self.tooltip.find("span", "q1")
        if span is None:
            return "None"
        return span.text if span.text else "None"

    def get_sockets(self):
        sockets = self.tooltip.find_all("a", "q0")
        socket_list = {}
        for s in sockets:
            s = s.text
            words = s.split(" ")
            if len(words) == 0:
                continue
            for colour in Item.SOCKET_COLOURS:
                if colour.value.lower() == words[0].lower():
                    if colour in socket_list:
                        socket_list[colour.name] = socket_list[colour.name] + 1
                    else:
                        socket_list[colour.name] = 1
        bonus = self.get_socket_bonus()
        if len(bonus) > 0:
            socket_list.update(bonus)
        return socket_list

    def get_socket_bonus(self):
        socket_bonus = self.tooltip.find("span", "q0")
        socket_bonus_pair = {}
        if socket_bonus is None:
            return socket_bonus_pair
        socket_bonus = socket_bonus.text
        for property_name in SingleItemParser.item_property_names:
            if re.search(property_name, socket_bonus, re.IGNORECASE):
                socket_bonus_pair[Item.PARAMETERS.SOCKET_BONUS.name] = {
                    property_name: re.search(r'\d+', socket_bonus).group()}
                return socket_bonus_pair


class ItemListParser:
    def __init__(self, service, url):
        self.url = url
        browser = _get_chrom_driver(service)
        browser.get(url)

        # TODO make this dynamic, use id = main-contents
        # time.sleep(5)
        content = browser.page_source

        self.soup_content = BeautifulSoup(content, "html.parser")
        # pprint(self.soup_content)
        self.soup_content = self.soup_content.find("div", attrs={'class': 'listview'})
        self.item_list = self.soup_content.find_all("a", attrs={'class': re.compile("q")}, href=re.compile("item="))
        # Closing Virtual Chrome browser after we are done
        browser.quit()

    def get_item_list(self):
        nice_item_list = {}
        for x in self.item_list:
            nice_item_list[x.text] = x['href']
        return nice_item_list


def _get_chrom_driver(service):
    chrome_options = webdriver.ChromeOptions()

    # Making the browser run in background and invisible
    chrome_options.add_argument('headless')
    chrome_options.add_argument('window-size=1920x1080')
    chrome_options.add_argument("disable-gpu")

    return webdriver.Chrome(service=service, options=chrome_options)

