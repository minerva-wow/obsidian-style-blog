# blog/management/commands/sync_content.py
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from blog.models import Post, Tag
from django.core.cache import cache
import os
import frontmatter
from django.conf import settings
import random

class Command(BaseCommand):
    help = 'Synchronize markdown content with database'
    
    # 预定义的标签颜色映射
    TAG_COLORS = {
        'python': '#3572A5',      # Python蓝
        'django': '#44B78B',      # Django浅绿
        'web': '#E44D26',         # HTML橙色
        'javascript': '#F0DB4F',  # JavaScript黄
        'css': '#264DE4',         # CSS蓝
        'react': '#61DAFB',       # React浅蓝
        'database': '#336791',    # PostgreSQL蓝
        'api': '#00FF00',         # API绿
        'tutorial': '#FF6B6B',    # 教程红
        'guide': '#4ECDC4',       # 指南青
    }
    
    # 备用颜色调色板
    COLOR_PALETTE = [
        "#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", 
        "#FFEEAD", "#D4A5A5", "#9B59B6", "#E67E22"
    ]

    def __init__(self):
        super().__init__()
        self.used_colors = set()

    def get_color_for_tag(self, tag_name):
        """为标签获取颜色"""
        # 检查预定义颜色
        tag_name_lower = tag_name.lower()
        if tag_name_lower in self.TAG_COLORS:
            return self.TAG_COLORS[tag_name_lower]
            
        # 从调色板选择颜色
        available_colors = [c for c in self.COLOR_PALETTE if c not in self.used_colors]
        if not available_colors:
            # 如果所有颜色都被使用了，重置使用过的颜色集合
            available_colors = self.COLOR_PALETTE
            self.used_colors.clear()
            
        color = random.choice(available_colors)
        self.used_colors.add(color)
        return color

    def process_tags(self, tags_data, post_obj):
        """处理文章的标签"""
        # 清除现有标签
        post_obj.tags.clear()
        
        for tag_data in tags_data:
            # 处理标签数据
            if isinstance(tag_data, dict):
                # 如果是字典格式（包含颜色信息）
                tag_name = tag_data.get('name')
                tag_color = tag_data.get('color')
            else:
                # 如果是简单的字符串格式
                tag_name = str(tag_data)
                tag_color = None
                
            if not tag_name:
                continue
                
            # 获取或创建标签
            tag, created = Tag.get_or_create_tag(tag_name)
            
            # 如果是新创建的标签或标签没有自定义颜色，设置颜色
            if created or tag.color == "#808080":
                # 优先使用明确指定的颜色
                if tag_color and tag_color.startswith('#'):
                    tag.color = tag_color
                else:
                    tag.color = self.get_color_for_tag(tag_name)
                tag.save()
                
            # 添加标签到文章
            post_obj.tags.add(tag)

    def sync_posts(self):
        """同步博客文章"""
        # 处理所有Markdown文件
        md_files = [f for f in os.listdir(settings.CONTENT_DIR) if f.endswith('.md') and f != 'about.md']
        
        for filename in md_files:
            self.stdout.write(f'Processing {filename}...')
            file_path = os.path.join(settings.CONTENT_DIR, filename)
            
            try:
                # 读取和解析markdown文件
                with open(file_path, 'r', encoding='utf-8') as f:
                    post = frontmatter.loads(f.read())
                
                # 从front matter获取数据
                title = post.get('title', filename.replace('.md', '').replace('-', ' ').title())
                slug = post.get('slug', slugify(title))
                tags = post.get('tags', [])

                # 创建或更新文章
                post_obj, created = Post.objects.update_or_create(
                    slug=slug,
                    defaults={
                        'title': title,
                        'content': post.content
                    }
                )

                # 处理标签
                self.process_tags(tags, post_obj)

                status = 'Created' if created else 'Updated'
                self.stdout.write(
                    self.style.SUCCESS(f'{status} post: {title}')
                )
                
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error processing {filename}: {str(e)}')
                )

    def sync_about(self):
        """同步about页面内容"""
        about_path = os.path.join(settings.CONTENT_DIR, 'about.md')
        if not os.path.exists(about_path):
            self.stdout.write('About.md not found, skipping...')
            return
            
        try:
            with open(about_path, 'r', encoding='utf-8') as f:
                about = frontmatter.loads(f.read())
                
            # 处理技术栈的颜色
            tech_stack = []
            for tech in about.get('tech_stack', []):
                tag = tech.get('tag', '').lower()
                name = tech.get('name', '')
                icon = tech.get('icon', '')
                
                # 使用对应标签的颜色
                color = self.TAG_COLORS.get(tag, self.get_color_for_tag(tag))
                
                tech_stack.append({
                    'name': name,
                    'color': color,
                    'icon': icon
                })
            
            # 处理项目的技术标签颜色
            projects = []
            for project in about.get('projects', []):
                techs = []
                for tech in project.get('technologies', []):
                    color = self.TAG_COLORS.get(tech.lower(), self.get_color_for_tag(tech))
                    techs.append({
                        'name': tech,
                        'color': color
                    })
                    
                projects.append({
                    'name': project['name'],
                    'description': project['description'],
                    'technologies': techs
                })
            
            # 构建完整的about内容
            about_content = {
                'title': about.get('title', 'About Me'),
                'subtitle': about.get('subtitle', ''),
                'introduction': about.get('introduction', ''),
                'tech_stack': tech_stack,
                'projects': projects,
                'contact': about.get('contact', {})
            }
            
            # 将内容保存到缓存
            cache.set('about_content', about_content, timeout=None)  # 永不过期
            
            self.stdout.write(
                self.style.SUCCESS('Successfully synced about page content')
            )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error processing about.md: {str(e)}')
            )

    def handle(self, *args, **options):
        """主处理函数"""
        self.stdout.write('Starting content synchronization...')
        
        # 确保内容目录存在
        content_dir = settings.CONTENT_DIR
        if not os.path.exists(content_dir):
            os.makedirs(content_dir)
            self.stdout.write(f'Created content directory at {content_dir}')

        # 加载现有标签的颜色
        existing_tags = Tag.objects.all()
        for tag in existing_tags:
            if tag.color != "#808080":
                self.used_colors.add(tag.color)

        # 同步文章
        self.sync_posts()
        
        # 同步about页面
        self.sync_about()

        self.stdout.write(self.style.SUCCESS('Content synchronization completed'))