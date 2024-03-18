from moviepy.editor import *
import ffmpeg
import os
import math


def process_video(input, output):
    """Parameter input should be a string with the full path for a video"""
    clip = VideoFileClip(input)
    duration_main = clip.duration
    durations = math.ceil((duration_main / 6))
    duration01 = durations
    duration02 = 2*durations
    duration03 = 3*durations
    duration04 = 4*durations
    duration05 = 5*durations
    duration06 = 6*durations
    
    width_a = clip.w - 10
    height_a = clip.h - 60
    print(clip.w,clip.h, clip.fps,duration01,duration02,duration03,duration04,duration05,duration06, duration_main)
    input_stream = ffmpeg.input(input)

    v0 = (input_stream.video.filter('trim', start=duration02, end=duration03)
          .filter('setpts', expr='PTS-STARTPTS').filter('setpts', expr='0.97*PTS')
          .filter('eq', contrast=0.96, brightness=0.020, saturation=1.10)
          .filter('rotate', a=-0.003))   
    a0 = (input_stream.audio.filter('atrim', start=duration02, end=duration03)
          .filter('asetpts', expr='PTS-STARTPTS').filter('atempo', 1.03).filter('volume', 0.85))
    
    v1 = (input_stream.video.filter('trim', start=duration03, end=duration04)
          .filter('setpts', expr='PTS-STARTPTS').filter('setpts', expr='0.99*PTS')
          .filter('eq', contrast=0.95, brightness=0.021, saturation=1.09).filter('rotate', a=-0.002))
    a1 = (input_stream.audio.filter('atrim', start=duration03, end=duration04)
          .filter('asetpts', expr='PTS-STARTPTS').filter('atempo', 1.01).filter('volume', 0.9))
    
   
   
    
    joined = ffmpeg.concat(v0, a0, v1, a1,v=1, a=1).node
    v8 = joined[0].filter('crop',width_a, height_a).filter('lut', a=155 * 0.5)
    a8 = joined[1]

    input_stream = ffmpeg.output(v8, a8, output, vcodec='libx264', map_metadata=-1,
                                 **{'metadata:g:0': f'title=dinhho', 'metadata:g:1': f'date=2024'})
    input_stream.run()


def get_video_paths(folder_path):
    """
    Parameter folder_path should look like "Users/documents/folder1/"
    Returns a list of complete paths
    """
    file_name_list = os.listdir(folder_path)

    path_name_list = []
    final_name_list = []
    for name in file_name_list:
        # Put any sanity checks here, e.g.:
        if name == ".DS_Store":
            pass
        else:
            path_name_list.append(folder_path + name)
            final_name_list.append(folder_path + "part 2_3_" + name)
    return path_name_list, final_name_list


if __name__ == "__main__":
    video_folder = input("What folder would you like to process? ")
    path_list, final_name_list = get_video_paths(video_folder)
    for path, name in zip(path_list, final_name_list):
        process_video(path, name)
    print("Finished")