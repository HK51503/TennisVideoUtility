import ffmpeg
import variables as var
import os
import datetime
import logging


def stitch_videos(destination_path, timestamp_file_path, is_keep_original):
    for match_id in var.dict_file_list:
        if len(var.dict_file_list[match_id]) != 0:
            # stitch videos
            f = open("concat.txt", "w", encoding="utf-8")
            f.writelines([('''file '%s'\n''' % input_path) for input_path in var.dict_file_list[match_id]])
            f.close()
            fn, extension = os.path.splitext(var.dict_file_list[match_id][0])
            file_name = match_id + extension
            file_path = os.path.join(destination_path, file_name)
            logging.info("Concatenating " + str(len(var.dict_file_list[match_id])) + " videos")
            ffmpeg.input("concat.txt", format="concat", safe="0").output(file_path, c="copy").run(overwrite_output=True)
            logging.info("Done concatenating")

            os.remove("concat.txt")

            var.dict_stitched_file[match_id] = file_path

            # create txt file with timestamps
            f = open(timestamp_file_path, "a")
            f.write(var.dict_match_id_full[match_id] + "\n")
            t = 0
            for index, file in enumerate(var.dict_file_list[match_id]):
                time = int(t)
                f.write(str(datetime.timedelta(seconds=time)) + " " + str(index+1) + "\n")
                duration = get_video_duration(file)
                t += duration
            f.write("\n")
            f.close()

            # remove original if keep original is false
            if is_keep_original == "False":
                for file in var.dict_file_list[match_id]:
                    os.remove(file)
                    logging.info("Finished removing file: " + os.path.basename(file))


def get_video_duration(video_path):
    video_info = ffmpeg.probe(video_path)
    duration = float(video_info["streams"][0]["duration"])
    return duration


if __name__ == "__main__":
    path = "/Users/kentezuka/Documents/GitHub/TennisVideoUtility/test/tmp/s1.mp4"
    get_video_duration(path)