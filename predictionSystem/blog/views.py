from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import Post  # Assuming your blog Post model is defined in models.py

def blog_list(request):
    # Retrieve all blog posts from the database
    blog_posts = Post.objects.all()
    
    # Pass the list of blog posts to the template for rendering
    return render(request, 'blog/blog.html', {'blog_posts': blog_posts})



from django.shortcuts import render, get_object_or_404
from django.utils.text import slugify  # Import slugify function
from .models import Post

# views.py
from django.shortcuts import render, get_object_or_404
import markdown
from django.utils.safestring import mark_safe
from .models import Post  # Import your Post model (update with your actual model)

def blog_post_detail(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    
    # Convert Markdown to HTML
    html_content = markdown.markdown(post.content)
    
    # Mark as safe to prevent HTML escaping
    safe_html_content = mark_safe(html_content)

    context = {
        'post': post,
        'safe_html_content': safe_html_content,  # Add the safe HTML content to the context
    }

    return render(request, 'blog/post_detail.html', context)
