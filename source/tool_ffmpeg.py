import ffmpeg
import variables as var
import os
import datetime
import logging
import requests
import zipfile
import shutil


def stitch_video(match_id, destination_path, timestamp_file_path, is_keep_original):
    # Set the path to your ffmpeg binaries
    ffmpeg_path = "resources/ffmpeg/bin"
    # Check if ffmpeg exists and download it if it doesn't
    ffmpeg_exists_check = 4 > len([f for f in os.listdir(ffmpeg_path) if os.path.isfile(os.path.join(ffmpeg_path, f))])
    if ffmpeg_exists_check:
        for file in os.listdir(ffmpeg_path):
            if file != "place.holder":
                os.remove(os.path.join(ffmpeg_path, file))
        download_ffmpeg()
    # Add the directory containing ffmpeg to the PATH environment variable
    os.environ["PATH"] = f"{ffmpeg_path}{os.pathsep}{os.environ.get('PATH', '')}"

    # stitch videos
    f = open("concat.txt", "w", encoding="utf-8")
    f.writelines([('''file '%s'\n''' % input_path) for input_path in var.dict_matches[match_id].file_list])
    f.close()
    fn, extension = os.path.splitext(var.dict_matches[match_id].file_list[0])
    file_name = match_id + extension
    file_path = os.path.join(destination_path, file_name)
    logging.info("Concatenating " + str(len(var.dict_matches[match_id].file_list)) + " videos")
    ffmpeg.input("concat.txt", format="concat", safe="0").output(file_path, c="copy").run(overwrite_output=True)
    logging.info("Done")

    os.remove("concat.txt")

    var.dict_matches[match_id].stitched_file = file_path

    # create txt file with timestamps
    f = open(timestamp_file_path, "a", encoding="utf-8")
    f.write(var.dict_matches[match_id].match_id_full + "\n")
    t = 0
    description = ""
    for index, file in enumerate(var.dict_matches[match_id].file_list):
        time = int(t)
        f.write(str(datetime.timedelta(seconds=time)) + " " + str(index + 1) + "\n")
        description += (str(datetime.timedelta(seconds=time)) + " " + str(index + 1) + "\n")
        duration = get_video_duration(file)
        t += duration
    var.dict_matches[match_id].youtube_upload_description = description
    f.write("\n")
    f.close()

    # remove original if keep original is false
    if is_keep_original == "False":
        for file in var.dict_matches[match_id].file_list:
            os.remove(file)
            logging.info("Finished removing file: " + os.path.basename(file))


def get_video_duration(video_path):
    video_info = ffmpeg.probe(video_path)
    duration = float(video_info["streams"][0]["duration"])
    return duration


def download_ffmpeg():
    destination_directory = "resources/ffmpeg"
    if var.platform == "windows":
        ffmpeg_url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
        file_name = "ffmpeg-release-essentials.zip"
        download_file(ffmpeg_url, file_name, destination_directory)
        with zipfile.ZipFile(os.path.join(destination_directory, file_name), "r") as ffmpeg_zip:
            selective_files = [f for f in ffmpeg_zip.namelist() if f[len(f) - 4:] == ".exe"]
            ffmpeg_folder_name = selective_files[0].split("/")[0]
            for file in selective_files:
                logging.info("Extracting " + file.split("/")[-1])
                ffmpeg_zip.extract(file, destination_directory)
        logging.info("Done extracting files")

        shutil.move(os.path.join(destination_directory, "bin", "place.holder"), os.path.join(destination_directory, ffmpeg_folder_name, "bin"))
        os.rmdir(os.path.join(destination_directory, "bin"))
        shutil.move(os.path.join(destination_directory, ffmpeg_folder_name, "bin"), "resources/ffmpeg/")
        os.remove(os.path.join(destination_directory, file_name))
        os.rmdir(os.path.join(destination_directory, ffmpeg_folder_name))

    elif var.platform == "darwin":
        ffmpeg_url = "https://evermeet.cx/ffmpeg/getrelease/ffmpeg/7z"
        ffmpeg_file_name = "ffmpeg.7z"
        ffprobe_url = "https://evermeet.cx/ffmpeg/getrelease/ffprobe/7z"
        ffprobe_file_name = "ffprobe.7z"
        ffplay_url = "https://evermeet.cx/ffmpeg/getrelease/ffplay/7z"
        ffplay_file_name = "ffplay.7z"
        download_file(ffmpeg_url, ffmpeg_file_name, destination_directory)
        download_file(ffprobe_url, ffprobe_file_name, destination_directory)
        download_file(ffplay_url, ffplay_file_name, destination_directory)
    elif var.platform == "linux":
        ffmpeg_url = "https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz"
        file_name = "ffmpeg-release-amd64-static.tar.xz"
        download_file(ffmpeg_url, file_name, destination_directory)
    else:
        logging.error("Platform not supported")
        """
        logic to stop process
        """



def download_file(url, file_name, destination_directory):
    file_path = os.path.join(destination_directory, file_name)
    logging.info("Downloading " + file_name + " from " + url)
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(file_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    logging.info("Done")

if __name__ == "__main__":
    var.platform = "windows"
    download_ffmpeg()
