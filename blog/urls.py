from django.urls import path
from .views import *

urlpatterns = [
    path('', PostList.as_view(), name='index'),
    path('post/<int:year>/<int:month>/<int:day>/<slug:slug>/', post_detail, name='post_detail'),
    path('share/<slug:slug>/', post_share, name='post_share')
]
