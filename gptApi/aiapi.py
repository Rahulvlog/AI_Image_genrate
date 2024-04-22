

import base64
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
# from googletrans import Translator
import cloudinary.uploader

change_settings({"IMAGEMAGICK_BINARY": "C:/Program Files/ImageMagick-7.1.1-Q16/magick.exe"})
# change_settings({"IMAGEMAGICK_BINARY": "/usr/bin/convert"})
X_API_KEY = "195bbfaa09c0ae854aa731a60a50d315e1655dd463bd7603f538c9cd3512fbd1" 


# translator = Translator()
openai.api_key = os.environ.get("OPENAI_API_KEY")
image_key = os.environ.get("image_key")
# cloudinary_config = os.environ.get("cloudinary_config")




def generateTitleResponse(user_input):
    model_engine = "gpt-3.5-turbo-instruct"
    prompt = user_input
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=150,
        n = 4,
        temperature=0.5,
    )
    
    try:
        temp = []
        for i, choice in enumerate(response.choices):
            temp.append(choice.text.strip().replace('\n', ''))
            temp[i] = temp[i].lstrip('1. ')
        
        return temp
    except (AttributeError, IndexError):
        choices = 'Oops, you beat the AI! Try a different question.'
    
    return choices


def editNewsResponse(user_input):
    model_engine = "gpt-3.5-turbo-instruct"
    prompt = user_input
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1000,
        temperature=0.5,
          top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    try:
        choices = response.choices[0].text
        
        with open("genrated_text.txt", "w") as file:
            file.write(choices.strip())
        
    except (AttributeError, IndexError):
        choices = 'Oops, you beat the AI! Try a different question.'
    
    return choices


# def rewrite_image(image):
#     img_bytes = io.BytesIO()
#     data = image.save(img_bytes, format="PNG")
#     print(data)
#     image_base64 = base64.b64encode(img_bytes.getvalue()).decode("utf-8")

#     # Encode the image_base64 as UTF-8 (not ASCII)
#     image_base64_utf8 = image_base64.encode('utf-8', 'ignore').decode()

#     # Split the prompt into smaller chunks
#     prompt = f"Please rewrite the image:\n{image_base64_utf8}"
#     chunks = [prompt[i:i+4090] for i in range(0, len(prompt), 4090)]

#     response_text = ""
#     for chunk in chunks:
#         while True:
#             try:
#                 response = openai.Completion.create(
#                     engine="text-davinci-002",
#                     prompt=chunk,
#                     max_tokens=150  # Adjust the max tokens as needed
#                 )
#                 response_text += response.choices[0].text
#                 break  # Exit the retry loop on success
#             except Exception as e:
#                 if "Rate limit reached" in str(e):
#                     # Wait for 20 seconds and then retry
#                     time.sleep(20)
#                 else:
#                     # Handle other exceptions
#                     raise e

#     # Extract the rewritten image from the response
#     rewritten_image_base64 = response_text
#     rewritten_image = Image.open(io.BytesIO(base64.b64decode(rewritten_image_base64)))

#     return rewritten_image


# convert the video

# def convert_video(user_input):
#     model_engine = "gpt-3.5-turbo-instruct"
#     prompt = user_input
#     response = openai.Completion.create(
#         engine=model_engine,
#         prompt=prompt,
#         max_tokens=1000,
#         temperature=0.5,
#           top_p=1.0,
#         frequency_penalty=0.0,
#         presence_penalty=0.0
#     )
#     try:
#         choices = response.choices[0].text.strip().replace('\n', '')
#         return choices
        
#         # with open("genrated_text.txt", "w") as file:
#         #     file.write(choices.strip())
        
#     except (AttributeError, IndexError):
#         choices = 'Oops, you beat the AI! Try a different question.'
    
#     return choices

   

def Image_converter(paragraphs):

    # i = 1
    # image_paths = []
    # for i, para in enumerate(paragraphs):
        
    response = requests.post(
        f"https://api.stability.ai/v2beta/stable-image/generate/core",
        headers={
            "authorization": f"Bearer {image_key}",
            "accept": "image/*"
        },
        files={
            "none": ''
        },
        data={
            "prompt": paragraphs,
            "output_format": "png",
        },
    )

    if response.status_code == 200:
        upload_result = cloudinary.uploader.upload(response.content, folder="images")
        # image_paths.append(upload_result['secure_url'])
        # image_path = f"./static/images/lighthouse{i}.png"
        # with open(image_path, 'wb') as file:
        #     file.write(response.content)
        # image_paths.append(image_path)
    else:
        raise Exception(str(response.json()))
    
    return upload_result['secure_url']
        # print(para)
        # response = openai.Image.create(
        #     prompt=para['text'],
        #     n=1,
        #     size="1024x1024"
        # )
       
        # image_url = response['data'][0]['url']
        # urllib.request.urlretrieve(image_url, f"static/images/image{i}.jpg")
        # print("The Generated Image Saved in Images Folder!")


def Audio_converter(paragraphs):
    # translator = Translator()
    # audio_files = [] 
    # for i, para in enumerate(paragraphs):
        # translated_text = translator.translate(para['text'], src='en', dest='hi')
    tts = gTTS(text=paragraphs, lang='hi', slow=False)
    audio_file_path = f"temp_voiceover_{1}.mp3"  # Corrected file extension to '.mp3'
    tts.save(audio_file_path)
    print(f"Saved audio file: {audio_file_path}")
    audio_result = cloudinary.uploader.upload(audio_file_path,  resource_type="video", folder="audios")
    # audio_files.append(audio_result['secure_url'])
    print("The Paragraph Converted into VoiceOver & Saved in Audio Folder!")
    return audio_result['secure_url']


def video_converter(paragraphs):
    i = 1
    for para in paragraphs:
        print("Extract voiceover and get duration...")
        audio_clip = AudioFileClip(para['audio'])
        audio_duration = audio_clip.duration
        
        print("Extract Image Clip and Set Duration...")
        image_url = para['image']
        image_clip = ImageClip(image_url).set_duration(audio_duration)

        print("Concatenate Audio and Image to Create Final Clip...")
        clip = image_clip.set_audio(audio_clip)

        video = CompositeVideoClip([clip])
        # video = f"video{i}.mp4"
        video_filename = f"static/videos/video{i}.mp4"
        video.write_videofile(video_filename, fps=24)
        # video = video.write_videofile(f"static/videos/video{i}.mp4", fps=24)
        print(f"The Video{i} Has Been Created Successfully!")
        upload_result = cloudinary.uploader.upload(video_filename, resource_type="video", folder="videos")
        # Get the public URL of the uploaded video
        public_url = upload_result["secure_url"]
         
        i+=1
        return public_url
    # return image_url
        
    # clips = []
    # l_files = os.listdir("static/videos")
    # for file in l_files:
    #     clip = VideoFileClip(f"static/videos/{file}")
    #     clips.append(clip)

    # print("Concatenate All The Clips to Create a Final Video...")
    # final_video = concatenate_videoclips(clips, method="compose")
    # final_video = final_video.write_videofile("static/final_video/final_video.mp4")
    # print("The Final Video Has Been Created Successfully!")
    



    

def final_converter(paragraphs):
    # paragraphs = text.split(". ")
    # print(paragraphs)
    # paragraphs = re.split(r"[,.]", text['text'])

    # Create Necessary Folders
    # os.makedirs("audio", exist_ok=True)
    # os.makedirs("images", exist_ok=True)
    # os.makedirs("videos", exist_ok=True)

    # Loop through each paragraph and generate an image for each
    i = 1
    for i, para in enumerate(paragraphs):
        # print(para)
        response = openai.Image.create(
            prompt=para['text'],
            n=1,
            size="1024x1024"
        )
        # print("Generate New AI Image From Paragraph...")
       
        image_url = response['data'][0]['url']
        # para['image'].replace(' ', '%20')   response['data'][0]['url']
        # print(image_url)
        urllib.request.urlretrieve(image_url, f"static/images/image{i}.jpg")
        print("The Generated Image Saved in Images Folder!")

        # Create gTTS instance and save to a file with Hindi language
        # translated_text = translator.translate(para['text'], src='en', dest='hi')
        tts = gTTS(text=para['text'].text, lang='hi', slow=False)
        tts.save(f"static/audio/voiceover{i}.mp3")
        print("The Paragraph Converted into VoiceOver & Saved in Audio Folder!")

        print("Extract voiceover and get duration...")
        audio_clip = AudioFileClip(f"static/audio/voiceover{i}.mp3")
        audio_duration = audio_clip.duration
        # Load the audio file using moviepy
        print("Extract Image Clip and Set Duration...")
        image_clip = ImageClip(f"static/images/image{i}.jpg").set_duration(audio_duration)

        # Use moviepy to create a text clip from the text
        print("Customize The Text Clip...")
        text_clip = TextClip(para['text'], fontsize=50, color="white")
        text_clip = text_clip.set_pos('center').set_duration(audio_duration)

        # Use moviepy to create a final video by concatenating
        # the audio, image, and text clips
        print("Concatenate Audio, Image, Text to Create Final Clip...")
        clip = image_clip.set_audio(audio_clip)
        video = CompositeVideoClip([clip, text_clip])

        # Save the final video to a file
        video = video.write_videofile(f"static/videos/video{i}.mp4", fps=24)
        print(f"The Video{i} Has Been Created Successfully!")
        i+=1


    clips = []
    l_files = os.listdir("static/videos")
    for file in l_files:
        clip = VideoFileClip(f"static/videos/{file}")
        clips.append(clip)

    print("Concatenate All The Clips to Create a Final Video...")
    final_video = concatenate_videoclips(clips, method="compose")
    final_video = final_video.write_videofile("static/final_video/final_video.mp4")
    print("The Final Video Has Been Created Successfully!")