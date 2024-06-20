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


def set_value(section, option, value):
    match_config = ConfigParser()
    match_config.read(var.match_config_file_name)
    match_config.set(section, option, value)

    with open(var.match_config_file_name, 'w') as configfile:
        match_config.write(configfile)


def read_value(section, option):
    match_config = ConfigParser()
    match_config.read(var.match_config_file_name)
    value = match_config[section][option]
    return value


def set_university(university):
    match_config = ConfigParser()
    match_config.read(var.match_config_file_name)
    match_config.set("settings", "university", university)

    with open(var.match_config_file_name, 'w') as configfile:
        match_config.write(configfile)


def read_university():
    match_config = ConfigParser()
    match_config.read(var.match_config_file_name)
    university_name = match_config["settings"]["university"]
    return university_name


def set_number_of_singles(singles):
    if singles.isdecimal() is True:
        match_config = ConfigParser()
        match_config.read(var.match_config_file_name)
        match_config.set("settings", "number_of_singles", singles)

        with open(var.match_config_file_name, 'w') as configfile:
            match_config.write(configfile)


def read_number_of_singles():
    match_config = ConfigParser()
    match_config.read(var.match_config_file_name)
    singles_number = match_config["settings"]["number_of_singles"]
    return singles_number


def set_number_of_doubles(doubles):
    if doubles.isdecimal() is True:
        match_config = ConfigParser()
        match_config.read(var.match_config_file_name)
        match_config.set("settings", "number_of_doubles", doubles)

        with open(var.match_config_file_name, 'w') as configfile:
            match_config.write(configfile)


def read_number_of_doubles():
    match_config = ConfigParser()
    match_config.read(var.match_config_file_name)
    doubles_number = match_config["settings"]["number_of_doubles"]
    return doubles_number
