# blog/views.py
from django.views.generic import ListView, DetailView, TemplateView
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Q
from django.core.cache import cache
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.http import JsonResponse
from django.contrib import messages
from .models import Post, Tag
from .forms import CommentForm

class GraphView(TemplateView):
    """图形视图作为首页"""
    template_name = 'blog/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        return context

class BasePostView:
    """基础视图类,提供共享功能"""
    model = Post
    
    def get_queryset(self):
        return super().get_queryset().prefetch_related('tags')

class PostListView(BasePostView, ListView):
    """文章列表视图"""
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = cache.get_or_set(
            'all_tags',
            lambda: Tag.objects.all(),
            60 * 60
        )
        return context

class PostDetailView(BasePostView, DetailView):
    """文章详情视图"""
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        slug = self.kwargs['slug']
        post = cache.get(f'post_detail_{slug}')
        
        if post is None:
            post = super().get_object(queryset)
            cache.set(f'post_detail_{slug}', post, 60 * 30)
            
        return post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs['slug']

        comments = cache.get(f'post_comments_{slug}')
        if comments is None:
            comments = self.object.comments.select_related('post').all()
            cache.set(f'post_comments_{slug}', comments, 60 * 5)
        
        context['comments'] = comments
        context['comment_form'] = CommentForm()
        return context

class TagPostListView(BasePostView, ListView):
    """标签文章列表视图"""
    template_name = 'blog/tag_posts.html'
    context_object_name = 'posts'
    paginate_by = 2

    def get_queryset(self):
        self.tag = get_object_or_404(Tag, name=self.kwargs['tag_name'])
        return super().get_queryset().filter(tags=self.tag)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        return context

class SearchView(BasePostView, ListView):
    """搜索视图"""
    template_name = 'blog/search.html'
    context_object_name = 'results'
    paginate_by = 2

    def get_queryset(self):
        query = self.request.GET.get('q', '').strip()
        if not query:
            return Post.objects.none()

        cache_key = f'search_{query}'
        results = cache.get(cache_key)

        if results is None:
            results = Post.objects.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(tags__name__icontains=query)
            ).distinct()
            cache.set(cache_key, results, 60 * 5)

        return results

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '').strip()
        return context

def ratelimit(request):
    client_ip = request.META.get('REMOTE_ADDR')
    cache_key = f'comment_rate:{client_ip}'
    
    if cache.get(cache_key, 0) >= 5:  # 5分钟5条评论
        return True
        
    cache.set(cache_key, cache.get(cache_key, 0) + 1, 300)
    return False


@require_POST
def add_comment(request, slug):
    if ratelimit(request):
        messages.error(request, 'Too many comments, try later')
        return redirect(f'{reverse("blog:post-detail", args=[slug])}#comments-section')
    
    """添加评论的视图函数"""
    post = get_object_or_404(Post, slug=slug)
    form = CommentForm(request.POST)
    
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        cache.delete(f'post_comments_{slug}')
    else:
        messages.error(request, 'Form validation failed')
        
    return redirect(f'{reverse("blog:post-detail", args=[slug])}#comments-section')

def graph_data(request):
    """图表数据API"""
    cache_key = 'graph_data'
    data = cache.get(cache_key)
    
    if data is None:
        posts = Post.objects.prefetch_related('tags').all()
        nodes = []
        links = []
        
        for post in posts:
            nodes.append({
                'id': f'post_{post.id}',
                'label': post.title,
                'type': 'post',
                'slug': post.slug
            })
            
            for tag in post.tags.all():
                tag_id = f'tag_{tag.id}'
                if not any(node['id'] == tag_id for node in nodes):
                    nodes.append({
                        'id': tag_id,
                        'label': tag.name,
                        'type': 'tag',
                        'color': tag.color
                    })
                links.append({
                    'source': f'post_{post.id}',
                    'target': tag_id
                })
        
        data = {'nodes': nodes, 'links': links}
        cache.set(cache_key, data, 60 * 60)
    
    return JsonResponse(data)

from django.shortcuts import render

def about(request):
    """关于页面视图"""
    about_content = cache.get('about_content', {})
    return render(request, 'blog/about.html', {
        'about_content': about_content
    })