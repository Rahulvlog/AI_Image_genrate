


import base64
import json
import openai
import os
from dotenv import load_dotenv
from PIL import Image
import io
import time

import requests
load_dotenv()
import os
import urllib.request
import cv2
import numpy as np
from gtts import gTTS
from moviepy.editor import *
from moviepy.config import change_settings
import openai
from googletrans import Translator
change_settings({"IMAGEMAGICK_BINARY": "C:/Program Files/ImageMagick-7.1.1-Q16/magick.exe"})
X_API_KEY = "195bbfaa09c0ae854aa731a60a50d315e1655dd463bd7603f538c9cd3512fbd1" 

translator = Translator()
def video_converter(paragraphs):
    # paragraphs = text.split(". ")
    print(paragraphs)

    # Create Necessary Folders
    # os.makedirs("audio", exist_ok=True)
    # os.makedirs("images", exist_ok=True)
    # os.makedirs("videos", exist_ok=True)

    # Loop through each paragraph and generate an image for each
    i = 1
    for para in paragraphs:
        image_url = convert_image_url(para)
        print(para)
        # response = openai.Image.create(
        #     prompt=para.strip(),
        #     n=1,
        #     size="1024x1024"
        # )
        print("Generate New AI Image From Paragraph...")
        image_url = image_url
        # print(image_url)
        req = urllib.request.Request(image_url, headers={'User-Agent': 'Mozilla/5.0'})

        # Use urlopen to open the URL and retrieve its content
        with urllib.request.urlopen(req) as response:
            image_content = response.read()

        # Save the retrieved content to a file
        with open(f"static/images/image{i}.jpg", "wb") as img_file:
            img_file.write(image_content)

        # Create gTTS instance and save to a file with Hindi language
        translated_text = translator.translate(para['text'], src='en', dest='hi')
        tts = gTTS(text=translated_text.text, lang='hi', slow=False)
        tts.save(f"static/audio/voiceover{i}.mp3")
        print("The Paragraph Converted into VoiceOver & Saved in Audio Folder!")
        
        print("Extract voiceover and get duration...")
        audio_clip = AudioFileClip(f"audio/voiceover{i}.mp3")
        audio_duration = audio_clip.duration
        # Load the audio file using moviepy
        print("Extract Image Clip and Set Duration...")
        image_clip = ImageClip(f"images/image{i}.jpg").set_duration(audio_duration)

        # Use moviepy to create a text clip from the text
        print("Customize The Text Clip...")
        text_clip = TextClip(para, fontsize=50, color="white")
        text_clip = text_clip.set_pos('center').set_duration(audio_duration)

        # Use moviepy to create a final video by concatenating
        # the audio, image, and text clips
        print("Concatenate Audio, Image, Text to Create Final Clip...")
        clip = image_clip.set_audio(audio_clip)
        video = CompositeVideoClip([clip, text_clip])

        # Save the final video to a file
        video = video.write_videofile(f"videos/video{i}.mp4", fps=24)
        print(f"The Video{i} Has Been Created Successfully!")
        i+=1


    clips = []
    l_files = os.listdir("videos")
    for file in l_files:
        clip = VideoFileClip(f"videos/{file}")
        clips.append(clip)

    print("Concatenate All The Clips to Create a Final Video...")
    final_video = concatenate_videoclips(clips, method="compose")
    final_video = final_video.write_videofile("final_video.mp4")
    print("The Final Video Has Been Created Successfully!")

    #     print("Extract voiceover and get duration...")
    #     audio_clip = AudioFileClip(f"static/audio/voiceover{i}.mp3")
    #     audio_duration = audio_clip.duration

    #     # Load the image file
    #     print("Extract Image Clip and Set Duration...")
    #     image = cv2.imread(f"static/images/image{i}.jpg")
    #     image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    #     h, w, _ = image.shape
    #     size = (w, h)
    #     duration = audio_duration

    #     # Define cartoonize function
    #     def cartoonize(image):
    #         gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    #         smooth = cv2.medianBlur(gray, 5)
    #         edges = cv2.adaptiveThreshold(smooth, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)

    #         color = cv2.bilateralFilter(image, 9, 300, 300)
    #         cartoon = cv2.bitwise_and(color, color, mask=edges)
    #         return cartoon

    #     # Apply cartoon effect to the image
    #     cartoon_image = cartoonize(image)

    #     # Create a video clip with cartoon images
    #     print("Creating Cartoon Video...")
    #     cartoon_images = [cartoon_image for _ in range(int(duration * 24))]
    #     clip = ImageSequenceClip(cartoon_images, fps=24)
    #     clip = clip.set_audio(audio_clip)
    #     clip = clip.set_duration(duration)
    #     clip.write_videofile(f"static/videos/video{i}.mp4", fps=24)
    #     print(f"The Video{i} Has Been Created Successfully!")
    #     i += 1


    # clips = []
    # l_files = os.listdir("static/videos")
    # for file in l_files:
    #     clip = VideoFileClip(f"static/videos/{file}")
    #     clips.append(clip)

    # print("Concatenate All The Clips to Create a Final Video...")
    # final_video = concatenate_videoclips(clips, method="compose")
    # final_video = final_video.write_videofile("final_video.mp4")
    # print("The Final Video Has Been Created Successfully!")
  

# def convert_image_url(para):
#     # Assuming this function returns the image URL based on the paragraph text
#     return 'https://img.midjourneyapi.xyz/sd/37462ae3-3bf9-44ba-b29a-2aa50a2dd386.png'  

def convert_image_url(imgae_text):
    url = 'https://api.midjourneyapi.xyz/sd/txt2img'

    headers = {
        'Content-Type': 'application/json',
        'X-API-KEY': '195bbfaa09c0ae854aa731a60a50d315e1655dd463bd7603f538c9cd3512fbd1'  # Replace 'YOUR_API_KEY_HERE' with your actual API key
    }

    data = {
        'prompt': imgae_text['text'],
        'model_id': 'midjourney',
        'width': '512',
        'height': '512'
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    res = response.json()
    if 'output' in res:
        result = ' '.join(res['output'])  # Joining list elements into a single string
        # result = result.replace('[', '').replace(']', '').split()
        return result
    else:
        print("Error: 'output' key not found in the response JSON.")
