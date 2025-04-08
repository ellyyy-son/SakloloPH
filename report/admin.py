from django.contrib import admin
from .models import Post, PostImage


class PostImageInline(admin.TabularInline):
    model = PostImage


class PostAdmin(admin.ModelAdmin):
    inlines = [PostImageInline]


admin.site.register(Post, PostAdmin)
admin.site.register(PostImage)