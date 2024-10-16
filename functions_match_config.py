import datetime, ast
from configparser import ConfigParser
import variables as var
from class_match import SinglesMatch, DoublesMatch

var.match_config_file_name = ""


def initialize():
    if var.match_config_file_name == "":
        var.match_date = str(datetime.date.today())
        var.match_config_file_name = "match_" + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + ".ini"
        var.default_match_config_file_name = var.match_config_file_name
        match_config = ConfigParser(allow_no_value=True)

        match_config.add_section("settings")
        match_config.set("settings", "match_date", var.match_date)
        match_config.set("settings", "university", "")
        match_config.set("settings", "number_of_singles", "0")
        match_config.set("settings", "number_of_doubles", "0")

        write_config(match_config)

    else:
        var.match_date = read_value("settings", "match_date")
        var.university_name = read_university()
        for i in range(int(read_number_of_singles())):
            match_id = "s" + str(i+1)
            match_id_hi = match_id.upper()
            var.dict_matches[match_id] = SinglesMatch(match_id)
            var.dict_matches[match_id].set_player(read_value(match_id_hi, "p"))
            try: var.dict_matches[match_id].file_list = ast.literal_eval(read_value(match_id_hi, "files"))
            except: pass
        for i in range(int(read_number_of_doubles())):
            match_id = "d" + str(i + 1)
            match_id_hi = match_id.upper()
            var.dict_matches[match_id] = DoublesMatch(match_id)
            var.dict_matches[match_id].set_player(read_value(match_id_hi, "p1"), read_value(match_id_hi, "p2"))
            try: var.dict_matches[match_id].file_list = ast.literal_eval(read_value(match_id_hi, "files"))
            except: pass


def add_section(section):
    match_config = ConfigParser()
    read_config(match_config)
    if match_config.has_section(section) is False: match_config.add_section(section)
    write_config(match_config)


def set_value(section, option, value):
    match_config = ConfigParser()
    read_config(match_config)
    match_config.set(section, option, value)
    write_config(match_config)


def read_value(section, option):
    match_config = ConfigParser()
    read_config(match_config)
    value = match_config[section][option]
    return value


def set_university(university):
    match_config = ConfigParser()
    read_config(match_config)
    match_config.set("settings", "university", university)

    write_config(match_config)


def read_university():
    match_config = ConfigParser()
    read_config(match_config)
    university_name = match_config["settings"]["university"]
    return university_name


def set_number_of_singles(singles):
    if singles.isdecimal() is True:
        match_config = ConfigParser()
        read_config(match_config)
        match_config.set("settings", "number_of_singles", singles)

        write_config(match_config)


def read_number_of_singles():
    match_config = ConfigParser()
    read_config(match_config)
    singles_number = match_config["settings"]["number_of_singles"]
    return singles_number


def set_number_of_doubles(doubles):
    if doubles.isdecimal() is True:
        match_config = ConfigParser()
        read_config(match_config)
        match_config.set("settings", "number_of_doubles", doubles)

        write_config(match_config)


def read_number_of_doubles():
    match_config = ConfigParser()
    read_config(match_config)
    doubles_number = match_config["settings"]["number_of_doubles"]
    return doubles_number


def if_match_exists():
    if read_number_of_singles() == "0" and read_number_of_doubles() == "0": return False
    else: return True


def read_config(match_config):
    match_config.read(var.match_config_file_name, encoding="utf-8")


def write_config(match_config):
    with open(var.match_config_file_name, 'w', encoding="utf-8") as configfile:
        match_config.write(configfile)
