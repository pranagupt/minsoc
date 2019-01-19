from django.urls import path
from . import views
from django.views.generic.base import TemplateView

app_name = 'blog'
urlpatterns = [
    path('',views.Home.as_view(), name = 'home'),
    path('<int:pk>/addcomment/', views.commentcreate, name = 'commentcreate'),
    path('profile/<str:username>',views.profile, name = 'profile'),
    path('post/edit/<int:pk>',views.postedit, name = 'post_edit'),
    path('post/delete/<int:pk>',views.postdelete, name = 'post_delete'),
    path('profile/edit/',views.ProfileEdit.as_view(), name = 'profile_edit'),
    path('signup/', views.SignUp.as_view(), name = 'signup'),
    path('postcreate/', views.PostCreate.as_view(), name = 'postcreate'),
    path('followedusersposts/', views.followedposts, name = 'followedposts'),
    path('follow/', views.follow, name = 'follow'),
    path('postsedited/<int:current_post_pk>', views.postsedited, name = 'postsedited'),
]
