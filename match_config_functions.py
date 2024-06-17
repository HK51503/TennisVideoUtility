import datetime
from configparser import ConfigParser
import variables as var

var.match_config_file_name = ""


def initialize():
    var.match_config_file_name = "match_" + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + ".ini"
    match_config = ConfigParser(allow_no_value=True)

    match_config.add_section("settings")
    match_config.set("settings", "match_date", "")
    match_config.set("settings", "university", "")
    match_config.set("settings", "number_of_singles", "0")
    match_config.set("settings", "number_of_doubles", "0")

    match_config.add_section("singles")
    match_config.add_section("doubles")

    match_config.write(open(var.match_config_file_name, "w"))

def set_university(university):
    match_config = ConfigParser()
    match_config.read(var.match_config_file_name)
    match_config.set("settings", "university", university)

def set_singles(singles):
    print("do it later")

def set_doubles(doubles):
    print("do it later")