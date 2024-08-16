from configparser import ConfigParser

config_file_name = "config.ini"


def set_value(section, option, value):
    settings_config = ConfigParser()
    read_config(settings_config)
    settings_config.set(section, option, value)

    write_config(settings_config)


def read_value(section, option):
    settings_config = ConfigParser()
    read_config(settings_config)
    value = settings_config[section][option]
    return value


def read_config(settings_config):
    settings_config.read(config_file_name, encoding="utf-8")


def write_config(settings_config):
    with open(config_file_name, 'w', encoding="utf-8") as configfile:
        settings_config.write(configfile)


if __name__ == "__main__":
    settings_config = ConfigParser()
    """
    settings_config.add_section("video_settings")
    set_value("video_settings", "youtube_upload", "False")
    set_value("video_settings", "stitch_videos", "False")
    set_value("video_settings", "keep_original", "False")
    """

    read_config(settings_config)
    settings_config.add_section("general_settings")
    write_config(settings_config)
    set_value("general_settings", "language", "ja")
