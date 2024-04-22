from django.urls import path
# from .views import login_view, register_user
from django.contrib.auth.views import LogoutView
from .views import *
# from django.views.decorators.csrf import csrf_exempt  

urlpatterns = [
    path('titlenews', OpenAIAPIView.as_view(), name="chatgpt"), 
    path('editnews', EditNewsView.as_view(), name="editnews"),
    # path('imagenews', ImageEditApi.as_view(), name="ImageEditApi"),
    path('imageGenrated', AiImageGenrated.as_view(), name="imageGenrated"),
    path('audioGenrated', AudioGenrated.as_view(), name="audioGenrated"),
    path('videoGenrated', VideoGenrated.as_view(), name="videoGenrated"),
    path('textConverter', TextConverterVideo.as_view(), name="textConverter"),
    path('postImage', SocialMediaAPIView.as_view(), name="postImage")

]
