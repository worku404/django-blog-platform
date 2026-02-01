from django.contrib import admin
"""This line came from django admin framework sothat i can create the admine site for my app
 django.contrib is a big subpackage that ahs auth sessions , staticfiles sites and other mmodules these are reusable app maintainded as part of django it self
 from here we import admin this gives as an interface that lets us to manage the database models 
 it provides other class such as modelAdmin register function @admin.register decorator
 admin configratio obtion llike filter search display and other"""
from .models import Post, Comment
"""here one this to remind dot means from the current folder from that we import our Post class"""
# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'status'] #it create tabular format for title slug author ... from the post class
    list_filter =  ['status', 'created', 'publish'] #it creats the filter page to filter basen on the status created and other
    prepopulated_fields = {'slug': ('title',)} #  this automatically populate the slug based on the text written in the titel space
    # raw_id_fields = ['author']
    date_hierarchy = 'publish'  #this create navigation bar based on the published fiels
    ordering = ['status', 'publish'] #this is the order of the posts in admin list page status first then puplish secod
    search_fields = ['title', 'body'] #this will create search bar ontop of the page , this look for title and the body
    
    """This block of code customize how the model appears and behaves in the django admin site
    here we inherited the class with the built in class admin.ModelAdmin so it can control and overide the built in class functionality
    here postAdmin controls the admin ui for post class"""

# this is for our comment section in admin page
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'user_email', 'post', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['user__name', 'user__email', 'body']
    def user_email(self, obj):
        return obj.user.email
    def user_name(self, obj):
        full_name = obj.user.get_full_name()
        return  full_name if full_name else obj.user.username
    user_email.short_description = 'User Email'