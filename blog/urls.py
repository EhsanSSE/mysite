from django.urls import path
from blog.views import *

app_name = 'blog'

urlpatterns = [
    path('', blog_view, name='index'),
    path('<int:pk>', blog_single, name='single'),
    path('category/<str:cat_name>', blog_view, name='category'),
    path('test', test_view)
]