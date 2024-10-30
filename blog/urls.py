from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('tag/<slug:tag_slug>/', post_list, name='index_by_tag'),
    path('post/<int:year>/<int:month>/<int:day>/<slug:slug>/', post_detail, name='post_detail'),
    path('share/<slug:slug>/', post_share, name='post_share'),
    path('send_comment/<slug:slug>/', comment_create, name='send_comment'),
    path('search/', search_with_indexing, name='search'),
]
