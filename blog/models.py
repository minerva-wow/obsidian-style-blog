# models.py
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
import markdown
from django.utils.html import escape
from django.conf import settings
from django.utils.functional import cached_property
from django.core.cache import cache

class Tag(models.Model):
    """标签模型 - 用于对文章进行分类"""
    name = models.CharField(max_length=100, unique=True)
    color = models.CharField(max_length=7, default="#808080")  # 用于前端展示的颜色

    class Meta:
        ordering = ['name']

    def get_absolute_url(self):
        return reverse('blog:tag-posts', args=[self.name])
    
    def save(self, *args, **kwargs):
        """保存时将标签名称转为小写"""
        self.name = self.name.lower()
        super().save(*args, **kwargs)

    @classmethod
    def get_or_create_tag(cls, name):
        """获取或创建标签（大小写不敏感）"""
        return cls.objects.get_or_create(name=name.lower())

class Post(models.Model):
    """文章模型 - 博客的核心内容"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['created_at']),
        ]

    def save(self, *args, **kwargs):
        # 自动生成slug
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:post-detail', args=[self.slug])

    def get_html_content(self):
        """将Markdown内容转换为HTML"""
        cache_key = f'post_html_{self.id}_{self.updated_at.timestamp()}'
        html = cache.get(cache_key)
        if html is None:
            html = markdown.markdown(
                self.content,
                extensions=settings.MARKDOWN_EXTENSIONS,
                extension_configs=settings.MARKDOWN_EXTENSION_CONFIGS
            )
            cache.set(cache_key, html, 3600 * 24)  # 缓存24小时
        return html

    @cached_property
    def get_reading_time(self):
        """估算阅读时间"""
        words_per_minute = 200
        word_count = len(self.content.split())
        return max(1, round(word_count / words_per_minute))

    def get_related_posts(self):
        """只关注数据获取逻辑"""
        return Post.objects.filter(tags__in=self.tags.all())\
                         .exclude(id=self.id)\
                         .select_related()\
                         .prefetch_related('tags')\
                         .distinct()[:3]

class Comment(models.Model):
    """评论模型 - 用于文章评论"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=10, blank=True)
    email = models.EmailField(blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['post', 'created_at']),
        ]

