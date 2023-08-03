from dataclasses import fields
from pydoc_data.topics import topics
from winreg import QueryInfoKey
from django.views.generic import View
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from .models import Board, Post
from django.contrib.auth.models import User
from .models import Post, Topic, Board
from .forms import NewTopicForm, PostForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.views.generic import UpdateView, ListView
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# Create your views here.

#GDBV
class ListBoards(ListView):
    model = Board
    template_name = "home.html"
    context_object_name = "boards"

# def home(request):
#     boards = Board.objects.all()
#     return render(request, "home.html", {'boards':boards})


def about(request):
    return HttpResponse(request, "ok")


def board_topics(request, boards_id):
    ##### method1 ######
    # try:
    #     board = Board.objects.get(pk=boards_id)
    # except Board.DoesNotExist:
    #     raise Http404
    board = get_object_or_404(Board, pk=boards_id)
    # i will add a virtual collumn called 'comments' assign to posts number in each topic
    # querySet => list of topics
    querySet = board.topics.order_by("-created_dt").annotate(comments = Count("posts"))
    # create a paginator of 20 topic/page
    paginator = Paginator(querySet, 20)
    page = request.GET.get('page', 1)   # page1 as default
    try:
        topics = paginator.page(page)  # topics => the topics in the page number=page
    except PageNotAnInteger:
        topics = paginator.page(1)
    except EmptyPage:
        topics = paginator.page(paginator.num_pages)

    return render(request, "topics.html", {"board":board, "topics":topics})


@login_required
def new_topic(request, boards_id):
    board = get_object_or_404(Board, pk=boards_id)
    # user = User.objects.first() XX

    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.created_by = request.user
            topic.save()

            post = Post.objects.create(
                message = form.cleaned_data.get('message'),
                topic = topic,
                created_by = request.user
            )

            return redirect(board_topics, boards_id=board.pk)
    else:
        form = NewTopicForm() 

    return render(request, "new_topic.html", {"board":board, "form":form})


def topic_posts(request, boards_id, topic_id):
    topic = get_object_or_404(Topic, board__pk=boards_id, pk=topic_id)

    # CREATE A UNIQUE SESSION FOR EACH VIEW OF TOPIC BY THE CURRENT USER
    session_key = "view_topic_{}"+format(topic.pk)
    if not request.session.get(session_key, False):
        topic.views += 1
        topic.save()
        request.session[session_key] = True

    return render(request, "topic_posts.html", {"topic":topic})


@login_required
def reply_topic(request, boards_id, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id, board__pk=boards_id)

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            form.save()
            # UPDATE TOPIC
            topic.updated_by = request.user
            topic.updated_dt = timezone.now()
            topic.save()

            return redirect(topic_posts, boards_id=topic.board.pk, topic_id=topic.pk)
    else:    
        form = PostForm()
    
    return render(request, "reply_topic.html", {"topic":topic, "form":form})


# I WILL USE HERE THE SECOND METHOD OF CREATEING A VIEW (GCBV)
@method_decorator(login_required, name="dispatch")  # you need to login to access the EDIT button
class UpdatePostView(UpdateView):
    model = Post
    fields = ('message',)
    template_name = 'edit_post.html'
    pk_url_kwarg = 'post_id'  # The pk_url_kwarg should be the name of the kwarg in the URL pattern(=post_id)
    context_object_name = 'post'  # the name of the object

    def form_valid(self, form):
        post = form.save(commit = False)
        post.updated_by = self.request.user
        post.updated_dt = timezone.now()
        post.save()
        return redirect('topic_posts', boards_id=post.topic.board.pk, topic_id=post.topic.pk)



#Update post with FBV
# def update_reply(request, boards_id, topic_id, post_id):
#     post = get_object_or_404(Post, pk=post_id, topic__pk=topic_id)
#     topic = get_object_or_404(Topic, pk=topic_id, board__pk=boards_id)
    
#     if request.method == 'POST':
#         form = PostForm(instance=post, data=request.POST)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.topic = topic
#             post.created_by = request.user
#             post.save()
#             return redirect(topic_posts, boards_id=post.topic.board.pk, topic_id=post.topic.pk)
#     else:
#         form = PostForm(instance=post)

#         return render(request, 'edit_post.html', {"post":post, "form":form})


# CLASS BASED VIEW-------------------------------------------------------------------------------
# We created a class named TaskCreateView and inherited CreateView. By doing that we gained a lot of functionality, with almost no code. Now we just need to set the following attributes:
# 1-model defines what Django model the view works with.
# 2-fields is used by Django to create a form (alternatively, we could provide form_class).
# 3-template_name defines which template to use (defaults to /<app_name>/<model_name>_form.html).
# 4-context_object_name defines the context key under which the model instance is passed to the template (defaults to object).
# 5-success_url defines where the user gets redirected on success (alternatively, you can set get_absolute_url in your model).
# -------------------------------------------------------------------------------------------------


# METHOD_2 : CLASS BASED VIEW -------------------------------------------------------------------------------
# DON'T FORGET TO PLACE THE URL IN URL.PY LIKE THAT : 
# path("boards/<int:boards_id>/topics/<int:topic_id>/reply", views.reply_topic.As_view(), name="reply_topic"),

# class ReplyTopic(View):
#     topic = get_object_or_404(Topic, pk=topic_id, board__pk=boards_id)

#     def render(self, request):
#         return render(request, "reply_topic.html", {"topic":topic, "form":form})

#     def post(self, request):
#         form = PostForm(request.POST)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.topic = topic
#             post.created_by = request.user
#             form.save()
#             return redirect(topic_posts, boards_id=topic.board.pk, topic_id=topic.pk)
#         return self.render(request)

#     def get(self, request):
#         form = PostForm()
#         return self.render(request)





# # METHOD_3 : GENERIC CLASS BASED VIEW --------------------------------------------------------------------------------
# class ReplyTopic(CreateView):
#     model = post
#     form_class = PostForm
#     success_url = reverse_lazy('post_list')
#     template_name = 'new_post.html'




# SIMPLE METHOD : FOR NEW TOPIC VIEW ----------------------------------------------------------------------------------
# def new_topic(request, boards_id):
#     board = get_object_or_404(Board, pk=boards_id)

#     if request.method == 'POST':
#         subject = request.POST['subject']
#         message = request.POST['message']
#         user = User.objects.first()

#         topic = Topic.objects.create(
#             subject = subject,
#             board = board,
#             created_by = user
#         )
#         post = Post.objects.create(
#             message = message,
#             topic = topic,
#             created_by = user
#         )

#         return redirect(board_topics, boards_id=board.pk)
#     return render(request, "new_topic.html", {"board":board})
