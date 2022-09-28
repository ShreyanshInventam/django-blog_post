from django.urls import path 
from .views import LoginAPIView, BlogAPIView
from .import views

urlpatterns = [
    path('login', LoginAPIView.as_view()),
    path('blog', BlogAPIView.as_view()),
    path('post', views.PostList, name='post'),
    path('tag-list', views.taglist),

]
