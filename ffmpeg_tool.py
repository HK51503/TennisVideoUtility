import ffmpeg
import variables as var
import os


def stitch_videos(destination_path):
    for match_id in var.dict_file_list:
        if len(var.dict_file_list[match_id]) != 0:
            input_paths = var.dict_file_list[match_id]
            f = open("concat.txt", "w")
            f.writelines([("file %s\n" % input_path) for input_path in input_paths])
            f.close()
            fn, extension = os.path.splitext(var.dict_file_list[match_id][0])
            file_name = match_id + extension
            file_path = os.path.join(destination_path, file_name)
            ffmpeg.input("concat.txt", format="concat", safe="0").output(file_path, c="copy").run()

            os.remove("concat.txt")

            var.dict_stitched_file[match_id] = file_path
