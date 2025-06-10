import os
import random

input_folder = 'input'
output_folder = 'output'
background_music = 'background.mp3'  # আপনার ব্যাকগ্রাউন্ড মিউজিক
logo_file = 'logo.png'               # আপনার লোগো

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

input_files = [f for f in os.listdir(input_folder) if f.endswith(('.mp4', '.mkv', '.avi'))]

if not input_files:
    print("❌ No video files found in input folder!")
    exit()

speed = round(random.uniform(0.95, 1.10), 2)
hue = random.randint(0, 45)
rotate = random.choice([0, 90, 180, 270])

rotate_filter = ""
if rotate == 90:
    rotate_filter = "transpose=1"
elif rotate == 180:
    rotate_filter = "transpose=2,transpose=2"
elif rotate == 270:
    rotate_filter = "transpose=2"

for input_file in input_files:
    input_path = os.path.join(input_folder, input_file)
    output_path = os.path.join(output_folder, f'edited_{input_file}')

    print(f"\n⏳ Editing: {input_file} with speed {speed}, hue {hue}, rotation {rotate} and adding logo")

    video_filters = f"{rotate_filter},crop=iw*0.95:ih*0.95,scale=1280:720,eq=brightness=0.05:contrast=1.3,hue=h={hue},drawbox=x=0:y=0:w=iw:h=ih:color=black@0.3:t=20"

    logo_filter = "movie='logo.png'[logo];[out][logo] overlay=W-w-10:10"

    filter_complex = f"[0:v]{video_filters}[out];{logo_filter};[0:a]atempo={speed},asetrate=44100*{speed},aresample=44100,volume=1.1[a1]; [1:a]volume=0.25[a2]; [a1][a2]amix=inputs=2:duration=first:dropout_transition=3"

    command = f'ffmpeg -i "{input_path}" -i "{background_music}" -i "{logo_file}" -filter_complex "{filter_complex}" -preset ultrafast "{output_path}" -y'

    os.system(command)
    print(f"✅ Done: {output_path}")

print("\n🎉 All files edited successfully with logo! Check the 'output' folder.")
