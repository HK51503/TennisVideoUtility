import argparse, os, ast
import variables as var
import functions_match_config as conf
import functions_settings_config as settings
from window_progress import main_process_logic

if __name__ == "__main__":
    print("Loading config file...")
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="Add match config file.", required=True, default="")
    args = parser.parse_args()
    if os.path.exists(args.config):
        var.match_config_file_name = args.config
    else:
        exit("Config file not found")

    conf.initialize()
    print("Done")

    print("Stitch videos:  " + settings.read_value("video_settings", "stitch_videos"))
    print("Keep original:  " + settings.read_value("video_settings", "keep_original"))
    print("YouTube upload: " + settings.read_value("video_settings", "youtube_upload"))
    i = 0
    while i < 1:
        confirmation = input("Do you want to run it with this configuration?y/n")[0].lower()

        if confirmation == "y":
            break
        elif confirmation == "n":
            exit("Please edit the config file and re-run the program")
        else:
            print("Please return a valid answer")

    for match_id in var.dict_matches:
        if conf.read_value(match_id.upper(), "files") != "[]":
            var.dict_matches[match_id].file_list = ast.literal_eval(conf.read_value(match_id.upper(), "files"))


    main_process_logic()


