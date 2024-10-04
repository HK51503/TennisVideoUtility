import variables as var
import os
import subprocess
import logging
import functions_match_config as conf
import shutil


def create_match_folder(directory):
    university_folder_name = str(conf.read_value("settings", "match_date") + " " + conf.read_value("settings", "university"))
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
    os.rename(original_file_path, destination_file_path)


def copy_videos(destination_directory_path):
    for match_id in var.dict_file_list:
        for index, original_file_path in enumerate(var.dict_file_list[match_id]):
            file_name = os.path.basename(original_file_path)
            logging.info("Copying file: " + file_name)
            shutil.copy2(original_file_path, destination_directory_path)
            logging.info("Finished copying: " + file_name)
            var.dict_file_list[match_id][index] = os.path.join(destination_directory_path, file_name)


def rename_videos(destination_directory_path):
    for match_id in var.dict_file_list:
        final_directory_path = os.path.join(destination_directory_path, var.dict_match_id_full[match_id])
        os.mkdir(final_directory_path)
        for index, original_file_path in enumerate(var.dict_file_list[match_id]):
            fn, file_extension = os.path.splitext(original_file_path)
            destination_file_name = var.university_name + " " + var.dict_match_id_full[match_id] + " " + str(index + 1) + file_extension
            rename_file(destination_file_name, original_file_path, final_directory_path)
            logging.info("Finished renaming file:" + os.path.basename(original_file_path))


def rename_stitched_videos(destination_directory_path):
    for match_id in var.dict_stitched_file:
        fn, file_extension = os.path.splitext(var.dict_stitched_file[match_id])
        destination_file_name = var.university_name + " " + var.dict_match_id_full[match_id] + file_extension
        rename_file(destination_file_name, var.dict_stitched_file[match_id], destination_directory_path)
        logging.info("Finished renaming file:" + os.path.basename(var.dict_stitched_file[match_id]))
        var.dict_youtube_upload[match_id].insert(0, destination_file_name)
        var.dict_youtube_upload[match_id].append(os.path.join(destination_directory_path, destination_file_name))


if __name__ == "__main__":
    # ディレクトリ情報を取得
    parent_dir = os.getcwd()

    # 大学名の入力、フォルダ作成、作業（？）ディレクトリの移動
    var.university_name = input("大学名？")
    path = create_match_folder(parent_dir)
    os.chdir(path)
    parent_dir = os.getcwd()

    # ダブルス、シングルスの本数を入力
    num_doubles = int(input("ダブルスの本数？"))
    num_singles = int(input("シングルスの本数？"))
    match_id_low_list = []

    # ダブルスフォルダ作成
    for i in range(num_doubles):
        match_id_low = "d" + str(i+1)
        match_id_hi = "D" + str(i+1)
        player_name_1 = input("%sの一人目の名前？" % match_id_hi)
        player_name_2 = input("%sの二人目の名前？" % match_id_hi)
        match_id_full = match_id_hi + " " + player_name_1 + " " + player_name_2
        match_folder_path = os.path.join(parent_dir, match_id_full)
        if not (os.path.exists(match_folder_path)):
            os.mkdir(match_folder_path)

        match_id_low_list.append(match_id_low)
        var.dict_match_id_full[match_id_low] = match_id_full

    # シングルスフォルダ作成
    for i in range(num_singles):
        match_id_low = "s" + str(i+1)
        match_id_hi = "S" + str(i+1)
        player_name = input("%sの一人目の名前？" % match_id_hi)
        match_id_full = match_id_hi + " " + player_name
        match_folder_path = os.path.join(parent_dir, match_id_full)
        if not (os.path.exists(match_folder_path)):
            os.mkdir(match_folder_path)

        match_id_low_list.append(match_id_low)
        var.dict_match_id_full[match_id_low] = match_id_full

    # 作成したフォルダをエクスプローラーで開く
    open_explorer = 'explorer.exe ' + '/root,"' + parent_dir + '"'
    print(open_explorer)
    subprocess.run(open_explorer)

    # 動画のコピー待ち
    print("フォルダに動画をコピーしてください")
    input("完了したらエンターキーを押してください")

    # 動画のファイル名変更および親ディレクトリへの動画の転送
    for i in range(num_singles + num_doubles):
        match_id_low = match_id_low_list[i]
        match_id_full = var.dict_match_id_full[match_id_low]
        path = os.path.join(parent_dir, match_id_full)
        cur_file_list = os.listdir(path)
        cur_file_list_full = []
        for file in cur_file_list:
            cur_file_list_full.append(os.path.join(path, file))

        var.dict_file_list[match_id_low] = cur_file_list_full

    rename_videos(parent_dir)

    print("ファイル名変更が完了しました")
