import glob
import os
import sys

from converter import Converter

conv = Converter()


def convert_to_mp4(video_file_path, output_file_path):
    info = conv.probe(video_file_path)

    convert = conv.convert(video_file_path, output_file_path, {
        'format': 'mp4',
        'video': {
            'codec': 'h264',
            'width': 720,
            'height': 720,
            'fps': 60
        }
    })

    for timecode in convert:
        pass

    print(f"Converted: {video_file_path} --> mp4")


if __name__ == '__main__':
    path = "human_eval_CRAFT_10K_balanced"

    for part in range(1, 6):
        for filepath in glob.iglob(f'{path}/videos/part_{part}/*.mpg'):
            id = filepath.split("/")[-1].split(".")[0]
            outfolder = f"{path}/videos_mp4/mp4_part_{part}"
            os.makedirs(outfolder, exist_ok=True)
            outpath = f"{outfolder}/{id}.mp4"
            convert_to_mp4(filepath, outpath)
