from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # 核心页面
    path('', views.GraphView.as_view(), name='home'),
    path('posts/', views.PostListView.as_view(), name='post-list'),
    path('post/<slug:slug>/', views.PostDetailView.as_view(), name='post-detail'),
    path('tag/<str:tag_name>/', views.TagPostListView.as_view(), name='tag-posts'),
    path('search/', views.SearchView.as_view(), name='search'),
     path('about/', views.about_view, name='about'),  # 添加 about 页面
    
    # API
    path('api/graph-data/', views.graph_data, name='graph-data'),
    path('post/<slug:slug>/comment/', views.add_comment, name='add-comment'),
]