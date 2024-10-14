import tool_rename, tool_ffmpeg, tool_youtube_upload
import os


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
    pass


def settings_menu():
    pass


def quit_app():
    pass


if __name__ == "__main__":
    main_menu()
