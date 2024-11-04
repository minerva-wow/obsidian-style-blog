# blog/management/commands/sync_content.py
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from blog.models import Post, Tag
import os
import frontmatter
from django.conf import settings

class Command(BaseCommand):
    help = 'Synchronize markdown content with database'

    def handle(self, *args, **options):
        self.stdout.write('Starting content synchronization...')
        
        content_dir = settings.CONTENT_DIR
        if not os.path.exists(content_dir):
            os.makedirs(content_dir)
            self.stdout.write(f'Created content directory at {content_dir}')

        # 获取所有.md文件
        md_files = [f for f in os.listdir(content_dir) if f.endswith('.md')]
        
        for filename in md_files:
            self.stdout.write(f'Processing {filename}...')
            file_path = os.path.join(content_dir, filename)
            
            try:
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
                post_obj.tags.clear()
                for tag_name in tags:
                    tag, _ = Tag.objects.get_or_create(
                        name=tag_name
                    )
                    post_obj.tags.add(tag)

                status = 'Created' if created else 'Updated'
                self.stdout.write(
                    self.style.SUCCESS(f'{status} post: {title}')
                )
                
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error processing {filename}: {str(e)}')
                )

        self.stdout.write(self.style.SUCCESS('Content synchronization completed'))