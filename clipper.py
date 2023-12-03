import glob
import os
import time

from pydub import AudioSegment

FIVE_MINUTE_WARNING_CLIP = AudioSegment.from_mp3("5-minute-warning.mp3")
ONE_MINUTE_WARNING_CLIP = AudioSegment.from_mp3("1-minute-warning.mp3")
ONE_MINUTE_SONG_CLIP = AudioSegment.from_mp3("William_Tell_Overture.mp3") + 6
ANTHEM_WARNING_CLIP = AudioSegment.from_mp3("please-rise-warning.mp3")
ANTHEM_SONG_CLIP = AudioSegment.from_mp3("O-Canada.mp3")

EXTENSION_LIST = ("*.m4a", "*.mp3")


def clip(source_dir_path, export_dir_path, fade_out=True, export_format='mp3', start=0):
    """
    Build Announcements Clips from a song source files.

    source_dir_path (str):
        path to source folder. ('m4a', 'mp3')

    export_dir_path (str)
        path to destination folder.

    fade_out (bool)
        cross-fades song and 1-minute warning.

    export_format (string)
        export file type. ('mp3', 'wav', 'raw', 'ogg' or other ffmpeg supported files)

    start (float)
        specific starting timestamp for song (s)
    """

    # remove '\' from ending of paths

    index = 0
    errors = 0

    start_time = time.time()

    os.chdir(source_dir_path)

    for extension in EXTENSION_LIST:
        for song_file in glob.glob(extension):
            try:
                song_filename = os.path.splitext(os.path.basename(song_file))[0]
                print(f"located song {index}: {song_filename}")

                export_path = f"{export_dir_path}\index-{index}({song_filename}).{export_format}"

                print(f"compiling mp3...")

                five_minute_song_clip = AudioSegment.from_file(song_file)[int(start * 1000):(4 * 60 - 22) * 1000]
                if fade_out:
                    five_minute_song_clip = five_minute_song_clip.fade_out(1 * 1000)

                new_clip = FIVE_MINUTE_WARNING_CLIP + five_minute_song_clip + \
                           ONE_MINUTE_WARNING_CLIP + ONE_MINUTE_SONG_CLIP + \
                           ANTHEM_WARNING_CLIP + ANTHEM_SONG_CLIP

                new_clip.export(export_path, format=export_format)

                print(f"finished building {export_path}")
            except:
                print(f"ran into error during building index:{index}.")

            index += 1

    print(f"process complete.")
    print(f"successfully built {index - errors}/{index} files in {time.time() - start_time}s")
