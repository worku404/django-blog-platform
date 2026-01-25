from django.urls import path
from . import  views
 
from .feeds import LatestPostsFeed
app_name = 'blog'
urlpatterns = [
    path(
        '',
        views.home,
        name='home'  
    ),
    path(
        'post/', 
        views.post_list, 
        name='post_list'
    ),
    path(
        'tag/<slug:tag_slug>/', 
        views.post_list,
        name='post_list_by_tag'
    ),
    path(
        'post/<int:year>/<int:month>/<int:day>/<slug:post>/',
        views.Post_detail, 
        name='post_detail'
    ),
    path(
        'kiya/',
        views.kiya_view,
        name='kiya'
    ),
    
    path(
        '<int:post_id>/share/',
        views.post_share,
        name='post_share'
    ),
    path(
        '<int:post_id>/comment/', 
        views.post_comment,
        name='post_comment'
    ),
    
    path('feed/',
         LatestPostsFeed(),
         name='post_feed'
        ),
    path(
        'search/',
        views.post_search,
        name='post_search'
    ),
    path(
        'llm/',
        views.llm_page,
        name='llm_page'
    ),
    path('llm/generate/',
         views.llm_generate,
         name='llm_generate'
         ), 
]