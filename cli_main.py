import tool_rename, tool_ffmpeg, tool_youtube_upload
import variables as var
import functions_match_config as conf
import os, argparse


def clear_console():

    # for windows
    if os.name == 'nt':
        _ = os.system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = os.system('clear')


def main_menu():
    clear_console()
    print("1.開始")
    print("2.試合を読み込み")
    print("3.試合を編集")
    print("4.設定")
    print("5.終了")
    i = input("選択:")
    if i == "1":
        start()
    elif i == "2":
        import_match_menu()
    elif i == "3":
        edit_match_menu()
    elif i == "4":
        settings_menu()
    elif i == "5":
        quit_app()
    else:
        main_menu()


def start():
    pass


def import_match_menu():
    pass


def edit_match_menu():
    print("")


def settings_menu():
    pass


def quit_app():
    clear_console()
    if input("本当に終了しますか？y/n:") == "y":
        clear_console()
    else:
        main_menu()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="Add match config file.", required=False, default="")
    args = parser.parse_args()
    if args.config:
        var.match_config_file_name = args.config

    conf.initialize()
    main_menu()
