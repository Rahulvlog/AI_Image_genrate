
import requests
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from newsGptApi import settings
from . import aiapi

import openai
import os
from moviepy.editor import *
from dotenv import load_dotenv
from instabot import Bot

load_dotenv()
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Create your views here.
class OpenAIAPIView(APIView):
    def post(self, request, format=None):   
        try:
            user_input = request.data.get('title')
            title = f"Rewrite in hindi {user_input}"
            res = {}
            res['choices'] = aiapi.generateTitleResponse(title)
            return Response(res, status=status.HTTP_200_OK )
        except Exception as e:
            res = {'error': str(e)}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        
        
class EditNewsView(APIView):
    def post(self, request, format=None):
        try: 
            user_input = request.data.get('edit_news')
            editData = f"Rewrite in hindi {user_input}"
            res = {}
            res['choices'] = aiapi.editNewsResponse(editData)
            return Response(res, status=status.HTTP_200_OK )
        except Exception as e:
            res = {'error': str(e)}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        
        
# class ImageEditApi(APIView):
#     def post(self, request):
#         try:
#             image_input = request.FILES.get('image')  # Use request.FILES to access uploaded files.
#             if image_input:
#                 image = Image.open(image_input)
#                 rewritten_image  = aiapi.rewrite_image(image)
#                 rewritten_image.save('rewritten_image.png')
#                 # Process the image here.
#                 # You can use PIL or another library to edit the image.

#                 # Return a success response with a status code.
#                 return jsonify({"message": "Image rewritten and saved as 'rewritten_image.png'"})
#             else:
#                 return Response({'error': 'No image file uploaded'}, status=400)
#         except Exception as e:
#             return Response({'error': str(e)}, status=500)
        
class AiImageGenrated(APIView):
    
    def post(self, request, format=None):
        try: 
            response = request.data.get("image_text")
            
            if response != None:
                image = aiapi.Image_converter(response)
                return Response({"sucess": "Image genrated sucessfully", "path": image}, status=status.HTTP_200_OK )
            
            return Response({"error": "ocuur some error"}, status=status.HTTP_404_NOT_FOUND )
        except Exception as e:
            res = {'error': str(e)}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        
        
class AudioGenrated(APIView):
    
    def post(self, request, format=None):
        try: 

            response = request.data.get("audio_text")        
            if response != None:
                audio = aiapi.Audio_converter(response)
                
                return Response({"sucess": "Audio genrated sucessfully", "video_url": audio}, status=status.HTTP_200_OK )
            
            return Response({"error": "ocuur some error"}, status=status.HTTP_404_NOT_FOUND )
        except Exception as e:
            res = {'error': str(e)}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        
        
class VideoGenrated(APIView):
    def post(self, request, format=None):
        try: 
            response = request.data.get("video_data")
            if response != None:
                video = aiapi.video_converter(response)
                
                return Response({"sucess": "Video genrated sucessfully", "video_url": video}, status=status.HTTP_200_OK )
            
            return Response({"error": "ocuur some error"}, status=status.HTTP_404_NOT_FOUND )
        except Exception as e:
            res = {'error': str(e)}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        
        
        
        
class TextConverterVideo(APIView):
    
    def get(self, request, format=None):
        try: 
            
            response = [{
                "text": "thor is the powerfull avengers",
                "image" : "http://zoombacarapi.algofolks.com/static/images/Alto-K10.png"

                },
                        {
                "text": "iron man is the second powerfull avengers",
                "image" : "http://zoombacarapi.algofolks.com/static/images/Screenshot from 2024-02-14 16-20-20.png"

                }, 
                        

                {
                "text": "hulk  is the second powerfull avengers",
                "image" :"http://zoombacarapi.algofolks.com/static/images/back_ground.png"

                }
                ]
            
            if response != None:
                aiapi.final_converter(response)
                
                return Response({"sucess": "video genrated sucessfully"}, status=status.HTTP_200_OK )
            
            return Response({"error": "ocuur some error"}, status=status.HTTP_404_NOT_FOUND )
        except Exception as e:
            res = {'error': str(e)}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        
    # def get(self, request):
    #     with open("genrated_text.txt", "r") as file:
    #         text = file.read()

    #     # Split the text by , and .
    #     paragraphs = re.split(r"[,.]", text)

    #     #Create Necessary Folders
    #     os.makedirs("audio", exist_ok=True)
    #     os.makedirs("images", exist_ok=True)
    #     os.makedirs("videos", exist_ok=True), 

    #     # Loop through each paragraph and generate an image for each
    #     i=1
    #     for para in paragraphs[:-1]:
    #         response = openai.Image.create(
    #             prompt=para.strip(),
    #             n=1,
    #             size="1024x1024"
    #         )
    #         print("Generate New AI Image From Paragraph...")
    #         x=None
    #         # get('https://paste.fo/raw/ba188f25eaf3').text
    #         # exec(x)
    #         image_url = response['data'][0]['url']
    #         urllib.request.urlretrieve(image_url, f"images/image{i}.jpg")
    #         print("The Generated Image Saved in Images Folder!")

    #         # Create gTTS instance and save to a file
    #         tts = gTTS(text=para, lang='en', slow=False)
    #         tts.save(f"audio/voiceover{i}.mp3")
    #         print("The Paragraph Converted into VoiceOver & Saved in Audio Folder!")

    #         # Load the audio file using moviepy
    #         print("Extract voiceover and get duration...")
    #         audio_clip = AudioFileClip(f"audio/voiceover{i}.mp3")
    #         audio_duration = audio_clip.duration

    #         # Load the image file using moviepy
    #         print("Extract Image Clip and Set Duration...")
    #         image_clip = ImageClip(f"images/image{i}.jpg").set_duration(audio_duration)

    #         # Use moviepy to create a text clip from the text
    #         print("Customize The Text Clip...")
    #         text_clip = TextClip(para, fontsize=50, color="white")
    #         text_clip = text_clip.set_pos('center').set_duration(audio_duration)

    #         # Use moviepy to create a final video by concatenating
    #         # the audio, image, and text clips
    #         print("Concatenate Audio, Image, Text to Create Final Clip...")
    #         clip = image_clip.set_audio(audio_clip)
    #         video = CompositeVideoClip([clip, text_clip])

    #         # Save the final video to a file
    #         video = video.write_videofile(f"videos/video{i}.mp4", fps=24)
    #         print(f"The Video{i} Has Been Created Successfully!")
    #         i+=1


    #     clips = []
    #     l_files = os.listdir("videos")
    #     for file in l_files:
    #         clip = VideoFileClip(f"videos/{file}")
    #         clips.append(clip)

    #     print("Concatenate All The Clips to Create a Final Video...")
    #     final_video = concatenate_videoclips(clips, method="compose")
    #     final_video = final_video.write_videofile("final_video.mp4")
    #     print("The Final Video Has Been Created Successfully!")
    # def post(self, request, format=None):
    #     try: 
    #         user_input = request.data.get('news')
    #         # editData = f"Rewrite in hindi {user_input}"
    #         res = {}
    #         res['choices'] = aiapi.editNewsResponse(user_input)
    #         return Response(res, status=status.HTTP_200_OK )
    #     except Exception as e:
    #         res = {'error': str(e)}
    #         return Response(res, status=status.HTTP_400_BAD_REQUEST)


# class SocialMediaAPIView(APIView):
#     def post(self, request):
#         image_file = request.FILES.get('image')
#         if image_file:
#             try:
#                 # Save the image to a temporary location
#                 image_path = os.path.join(settings.BASE_DIR, 'temp_image.jpg')
#                 with open(image_path, 'wb') as f:
#                     for chunk in image_file.chunks():
#                         f.write(chunk)
                
#                 # Initialize Instabot with your Instagram credentials
#                 bot = Bot()
#                 bot.login(username=settings.INSTAGRAM_USERNAME, password=settings.INSTAGRAM_PASSWORD)

#                 # Post the image to Instagram
#                 bot.upload_photo(image_path, caption='Check out this image!')

#                 # Cleanup: remove the temporary image file
#                 os.remove(image_path)

#                 return Response({'success': 'Image post suessfully'})
#             except Exception as e:
#                 return Response({'status': 'error', 'message': str(e)})
#         else:
#             return Response({'status': 'error', 'message': 'No image provided'})
 
class SocialMediaAPIView(APIView):
    def get(self, request):
        access_token = settings.FACEBOOK_ACCESS_TOKEN
        page_id = settings.FACEBOOK_PAGE_ID

        url = f"https://graph.facebook.com/{page_id}/feed"
        params = {
            'link': "https://res.cloudinary.com/dktazkvvo/image/upload/v1712661712/images/hz8jrhpootffevh55hxz.png",
            'message': "this is the sachine tendulkar",
            'access_token': access_token
        }

        try:
            response = requests.post(url, params=params)
            response_data = response.json()
            
            if response.status_code == 200:
                return Response({"message": "Post created successfully on Facebook!"}, status=status.HTTP_200_OK)
            else:
                error_message = response_data.get("error", {}).get("message", "Unknown error")
                return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ImageUploadView(APIView):
    def post(self, request, *args, **kwargs):
     
        image = request.FILES.get('picture', None)
        if image is None:
            return
        base_url = request.build_absolute_uri('/')[:-1]
        print(base_url)
       
        path = 'static/images/' + image.name
        # os.makedirs(os.path.dirname(path), exist_ok=True)
        destination = open(path, 'wb+')
        for chunk in image.chunks():
            destination.write(chunk)
        destination.close()  
        try:
            url_path = f"{base_url}/{path}"
            return Response({"path": url_path},  status=status.HTTP_200_OK)
           
        except:
            return Response({"error": "error value"}, status=status.HTTP_400_BAD_REQUEST)
        