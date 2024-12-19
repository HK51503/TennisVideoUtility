import variables as var
import os
import subprocess
import logging
import functions_match_config as conf
import shutil
import datetime
from class_match import SinglesMatch, DoublesMatch


def create_match_folder(directory):
    university_folder_name = str(var.match_date + " " + var.university_name)
    university_folder_path = os.path.join(directory, university_folder_name)
    logging.info("Checking if folder: %s exists" % university_folder_name)
    if not (os.path.exists(university_folder_path)):
        os.mkdir(university_folder_path)
        logging.info("Creating folder: " + university_folder_name)
    else:
        logging.info("Folder already exists")
    return university_folder_path


def rename_file(destination_file_name, original_file_path, destination_directory_path):
    destination_file_path = os.path.join(destination_directory_path, destination_file_name)
    if os.path.exists(destination_file_path):
        os.remove(destination_file_path)
    os.rename(original_file_path, destination_file_path)


def copy_video(match_id, destination_directory_path):
    for index, original_file_path in enumerate(var.dict_matches[match_id].file_list):
        file_name = os.path.basename(original_file_path)
        logging.info("Copying file: " + file_name)
        shutil.copy2(original_file_path, destination_directory_path)
        logging.info("Finished copying: " + file_name)
        var.dict_matches[match_id].file_list[index] = os.path.join(destination_directory_path, file_name)


def rename_videos(match_id, destination_directory_path):
    final_directory_path = os.path.join(destination_directory_path, var.dict_matches[match_id].match_id_full)
    if os.path.exists(final_directory_path) is False:
        os.mkdir(final_directory_path)
    for index, original_file_path in enumerate(var.dict_matches[match_id].file_list):
        fn, file_extension = os.path.splitext(original_file_path)
        destination_file_name = var.university_name + " " + var.dict_matches[match_id].match_id_full + " " + str(
            index + 1) + file_extension
        rename_file(destination_file_name, original_file_path, final_directory_path)
        logging.info("Finished renaming file:" + os.path.basename(original_file_path))


def rename_stitched_video(match_id, destination_directory_path):
    fn, file_extension = os.path.splitext(var.dict_matches[match_id].stitched_file)
    destination_file_name = var.university_name + " " + var.dict_matches[match_id].match_id_full + file_extension
    rename_file(destination_file_name, var.dict_matches[match_id].stitched_file, destination_directory_path)
    logging.info("Finished renaming file:" + os.path.basename(var.dict_matches[match_id].stitched_file))
    youtube_title, file_extension_2 = os.path.splitext(destination_file_name)
    var.dict_matches[match_id].youtube_upload_title = youtube_title
    var.dict_matches[match_id].youtube_upload_file_path = os.path.join(destination_directory_path,
                                                                       destination_file_name)


if __name__ == "__main__":
    # ディレクトリ情報を取得
    parent_dir = os.getcwd()

    # 大学名の入力、フォルダ作成、作業（？）ディレクトリの移動
    var.match_date = str(datetime.date.today())
    var.university_name = input("大学名？")
    path = create_match_folder(parent_dir)
    os.chdir(path)
    parent_dir = os.getcwd()

    # ダブルス、シングルスの本数を入力
    num_doubles = int(input("ダブルスの本数？"))
    num_singles = int(input("シングルスの本数？"))
    match_id_low_list = []

    # ダブルス、シングルスのインスタンスを作成
    for i in range(num_doubles):
        match_id = "d" + str(i+1)
        var.dict_matches[match_id] = DoublesMatch(match_id)
    for i in range(num_singles):
        match_id = "s" + str(i+1)
        var.dict_matches[match_id] = SinglesMatch(match_id)

    # ダブルスフォルダ作成
    for i in range(num_doubles):
        match_id_low = "d" + str(i+1)
        match_id_hi = "D" + str(i+1)
        player_name_1 = input("%sの一人目の名前？" % match_id_hi)
        player_name_2 = input("%sの二人目の名前？" % match_id_hi)
        var.dict_matches[match_id_low].set_player(player_name_1, player_name_2)
        match_id_full = var.dict_matches[match_id_low].match_id_full
        match_folder_path = os.path.join(parent_dir, match_id_full)
        if not (os.path.exists(match_folder_path)):
            os.mkdir(match_folder_path)

    # シングルスフォルダ作成
    for i in range(num_singles):
        match_id_low = "s" + str(i+1)
        match_id_hi = "S" + str(i+1)
        player_name = input("%sの一人目の名前？" % match_id_hi)
        var.dict_matches[match_id_low].set_player(player_name)
        match_id_full = var.dict_matches[match_id_low].match_id_full
        match_folder_path = os.path.join(parent_dir, match_id_full)
        if not (os.path.exists(match_folder_path)):
            os.mkdir(match_folder_path)

    # 作成したフォルダをエクスプローラーで開く
    open_explorer = 'explorer.exe ' + '/root,"' + parent_dir + '"'
    print(open_explorer)
    subprocess.run(open_explorer)

    # 動画のコピー待ち
    print("フォルダに動画をコピーしてください")
    input("完了したらエンターキーを押してください")

    # 動画のファイル名変更および親ディレクトリへの動画の転送
    for match_id in var.dict_matches:
        match_id_full = var.dict_matches[match_id].match_id_full
        path = os.path.join(parent_dir, match_id_full)
        cur_file_list = os.listdir(path)
        cur_file_list_full = []
        for file in cur_file_list:
            cur_file_list_full.append(os.path.join(path, file))

        var.dict_matches[match_id].file_list = cur_file_list_full
        if var.dict_matches[match_id].file_list:
            rename_videos(match_id, parent_dir)

    print("ファイル名変更が完了しました")
