from django.db import models
from django.utils.text import slugify
class Post(models.Model):
    

    level = models.CharField(max_length=20, default="No Level Specified")
    title = models.CharField(max_length=200)
    description = models.TextField(default="No description available.")
    content = models.TextField()
    slug = models.SlugField(max_length=100, unique=True, db_index=True, default= "no-slug-description", blank=True)
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    image = models.ImageField(upload_to='blog_images/', default='blog_images/default.jpg')
    # Assumes you have an 'uploads' directory in your MEDIA_ROOT

    def save(self, *args, **kwargs):
        if not self.slug:
            # Generate the slug from the title
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title