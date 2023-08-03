from unicodedata import name
from django.urls import path
from boards import views

urlpatterns = [
    # path("", views.home, name="home"),    # Default method
    path("", views.ListBoards.as_view(), name="home"),  # GDBV method
    path("about/", views.about, name="about"),
    path("boards/<int:boards_id>", views.board_topics, name="board_topics"),
    path("boards/<int:boards_id>/new/", views.new_topic, name="new_topic"),
    path("boards/<int:boards_id>/topics/<int:topic_id>", views.topic_posts, name="topic_posts"),
    path("boards/<int:boards_id>/topics/<int:topic_id>/reply", views.reply_topic, name="reply_topic"),
    path("boards/<int:boards_id>/topics/<int:topic_id>/posts/<int:post_id>", views.UpdatePostView.as_view(), name="edit_post"),
]
