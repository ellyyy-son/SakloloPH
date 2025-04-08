from django.db import models
from django.urls import reverse


CATEGORY_CHOICES = [
    ('Land', 'Land'),
    ('Water', 'Water'),
    ('Electricity', 'Electricity'),
    ('Miscellaneous', 'Miscellaneous')
]


class Post(models.Model):
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    location = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    is_resolved = models.BooleanField(default=False)

    def vote_score(self):
        return self.upvotes - self.downvotes

    def __str__(self):
        return f"{self.category} issue at {self.location}"

    def get_absolute_url(self):
        return reverse('report:post_detail', args=[str(self.pk)])


class PostImage(models.Model):
    image = models.ImageField(upload_to='post_images/', null=True)
    description = models.TextField(max_length=255, null=True, blank=True)
    post = models.ForeignKey(Post, related_name='images', on_delete=models.CASCADE)

    def __str__(self):
        return f"Image for post {self.post.title}"