from django.views.generic import ListView #this is for class based view
from django.shortcuts import get_object_or_404, render
from .models import Post #this fetch data from post class
# creating post share view
from django.conf import settings  #  access DEFAULT_FROM_EMAIL / mail backend
from django.core.mail import send_mail
from django.views.decorators.http import require_POST

from django.contrib.postgres.search import TrigramSimilarity
# import redis

from .form import (EmailPostForm, 
                   CommentForm, 
                   SearchForm,
                   LLMForm,
                #    LoginForm
                   ) # validate share-by-email inputs and  # needed for Post_detail
from django.contrib.postgres.search import (SearchVector, 
                                            SearchQuery,
                                            SearchRank
                                            )

from django.db.models import Count
from taggit.models import Tag
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import requests
from django.http import JsonResponse,HttpResponse

import os
from dotenv import load_dotenv
import markdown

from django.contrib.auth.decorators import login_required

@login_required
def Post_detail(request, year, month, day, slug, post_id): #here we have to pass the arguments here inorder to display the revered url.
    post = get_object_or_404( #this help as to catch the error without using try and except method.
        Post,
        status = Post.Status.PUBLISHED, #return only published post
        slug = slug,
        publish__year = year,
        publish__month=month,
        publish__day=day,
        id=post_id
    )
    
    # then go to templates list.html
    #list of active comments for this post
    all_comments = post.comments.filter(active=True).order_by("-created") 
    total_comments = all_comments.count()
    try:
        comment_limit = int(request.GET.get("climit", 3))
    except (ValueError, TypeError):
        comment_limit = total_comments
    
    #clamp to sane bounds
    comment_limit = max(0, min(comment_limit, total_comments))
    
    comments = all_comments[:comment_limit]
    has_more_comments = comment_limit < total_comments
    next_comment_limit = min(comment_limit+5, total_comments)
    # --- end comments ---
    # form for users to comment
    comment_form = CommentForm()
    llm_form = LLMForm()
    #list of similar posts
    post_tag_ids = post.tags.values_list('id', flat = True)
    # INCREMENT TOTAL POST VIEW BY ONE
    # total_views = r.incr(f'post:{post.id}: views')
    similar_posts = (
        Post.published
        .filter(tags__in = post_tag_ids)
        .exclude(id=post.id)
        )
    similar_posts = (
        similar_posts
        .annotate(same_tags = Count('tags'))
        .order_by('-same_tags', '-publish')
        )[:4]
    
    return render(
        request, 
        'blog/post/detail.html',
        {
            'post': post,
            'comments': comments,
            'total_comments': total_comments,
            'has_more_comments': has_more_comments,
            'next_comment_limit': next_comment_limit,
            'comment_limit': comment_limit,
            'llm_form': llm_form,
            'comment_form': comment_form,
            'similar_posts':similar_posts
            # 'total_views':total_views
        }
    )
    
@login_required
def post_list(request, tag_slug = None):
    
    llm_form = LLMForm()
    post_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
        
    #--pagination with 3 posts per page
    paginator = Paginator(post_list, 4) #from all published item take only three items.
    page_number = request.GET.get('page', 1)#  read ?page= from query string; default to page 1 if missing.
    try:
        page_obj = paginator.page(page_number)
    except EmptyPage:
        #If page_number is out of range get last page of result
        page_obj=paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    
    return render(
        request,
        'blog/post/list.html',
        {'posts': post_list,
         'page_obj': page_obj,
         'tag': tag,
         'llm_form':llm_form
        }
    )
def kiya_view(request):
    return render(
        request, 
        'blog/post/kiya.html'
    )
def home(request):
    return render(
        request, 
        'blog/post/home.html'
    )
@login_required
def post_share(request, post_id):
    llm_form = LLMForm()
    post = get_object_or_404(
        Post,
        id=post_id,
        status=Post.Status.PUBLISHED
    )
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url()
            )
            subject = f"{cd['name']} ({cd['email']}) recommends you read {post.title}"
            message = (
                f"Read {post.title} at {post_url}\n\n"
                f"{cd['name']}'s comments: {cd['comments']}"
            )
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[cd['to']],
            )
            sent = True
    else:
        form = EmailPostForm()
    return render(
        request,
        'blog/post/share.html',
        {
            'post': post,
            'form': form,
            'sent': sent,
            'llm_form':llm_form
        }
    )
  #  ensure only POST requests are allowed
@require_POST
def post_comment(request, post_id):
    llm_form = LLMForm()
    post = get_object_or_404(  #  fetch the post or return 404 if not found
        Post,
        id=post_id,
        status=Post.Status.PUBLISHED
    )
    comment = None  #  initialize the comment variable
    form = CommentForm(data=request.POST)  #  bind the form to the submitted data
    if form.is_valid():  #  validate the form data
        comment = form.save(commit=False)  #  create a comment object without saving
        comment.post = post  #  associate the comment with the post
        comment.user = request.user
        comment.name = request.user.username # set name from user
        comment.save()  #  save the comment to the database
    return render(  #  render the response with the post, form, and comment
        request,
        'blog/post/comment.html',
        {
            'post': post,
            'form': form,
            'comment': comment,
            'llm_form': llm_form
        }
    )
@login_required   
def post_search(request):
    form = SearchForm()
    llm_form = LLMForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector(
                'title', weight = 'A'
                ) + SearchVector(
                    'body', weight = "B"
                    )
            search_query = SearchQuery(query)
            results = (
                Post.published.annotate(
                    # search = search_vector,
                    # rank = SearchRank(search_vector, search_query),
                    similarity = TrigramSimilarity('title', query),
                )
                .filter(similarity__gt = 0.1)
                .order_by('-similarity')
            )
    return render(
        request,
        'blog/post/search.html',
        {
            'form': form,
            'query': query,
            'results': results,
            'llm_form': llm_form
        }
    )

env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'foodie', '.env')
load_dotenv(dotenv_path=env_path)
@require_POST
@login_required
def post_like(request):
    post_id = request.POST.get('id')
    action = request.POST.get('action')

    if post_id and action:
        try:
            post = Post.objects.get(id=post_id)

            if action == 'like':
                post.users_like.add(request.user)
            else:
                post.users_like.remove(request.user)

            return JsonResponse({
                'status': 'ok',
                'total_likes': post.users_like.count()
            })

        except Post.DoesNotExist:
            return JsonResponse({'status': 'error'})

    return JsonResponse({'status': 'error'})

# r = redis.Redis(
#     host=settings.REDIS_HOST,
#     port=settings.REDIS_PORT,
#     db=settings.REDIS_DB
# )
@require_POST
@login_required
def llm_generate(request):
    prompt = (request.POST.get("prompt") or "").strip()
    if not prompt:
        return JsonResponse({"error": "Prompt is required."}, status=400)

    # Get prior history from session (list of {"prompt":..., "response":...})
    url = "https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent"
    history = request.session.get("llm_history", [])

    # Optional: limit memory to last N turns to avoid token overflow
    max_turns = 3
    history = history[-max_turns:]

    # Build Gemini contents from history + new prompt
    contents = []
    for item in history:
        if item.get("prompt"):
            contents.append({"role": "user", "parts": [{"text": item["prompt"]}]})
        if item.get("response"):
            contents.append({"role": "model", "parts": [{"text": item["response"]}]})

    contents.append({"role": "user", "parts": [{"text": prompt}]})

    data = {"contents": contents}

    # Call Gemini (your existing API loop)
    api_keys = [
            os.getenv("GEMINI_API_KEY_1"),
            os.getenv("GEMINI_API_KEY_2"),
            os.getenv("GEMINI_API_KEY_3"),
            os.getenv("GEMINI_API_KEY_4"),
        ]
    last_error = None
    for api_key in api_keys:
        if not api_key:
            continue
        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": api_key
        }
        try:
            response = requests.post(url, headers=headers, json=data, timeout=20)
            if response.status_code == 200:
                content = response.json()
                generated = content["candidates"][0]["content"]["parts"][0]["text"]

                # Save new turn to session
                history.append({"prompt": prompt, "response": generated})
                request.session["llm_history"] = history
                request.session.modified = True

                # Return HTML for display
                return JsonResponse({"generated": markdown.markdown(generated)})
            last_error = {"status": response.status_code}
        except Exception as exc:
            last_error = {"error": str(exc)}
            continue

    return JsonResponse(
        {
            "error": "All API keys failed or quota exceeded.",
            "details": last_error,
        },
        status=500,
    )

@login_required
def llm_page(request):
    llm_form = LLMForm()
    history = request.session.get("llm_history", [])

    # Convert response text to HTML for display
    history_ui = [
        {"prompt": h["prompt"], "response": markdown.markdown(h["response"])}
        for h in history
    ]

    return render(
        request,
        "blog/post/llm_page.html",
        {"llm_form": llm_form, 
         "llm_history": history_ui
         }
    )
