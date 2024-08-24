from django.shortcuts import render
from .models import Blog
from django.core.paginator import Paginator

def blog_list(request):
    blogs = Blog.objects.all().order_by('-created_at')
    paginator = Paginator(blogs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blogs/blog_list.html', {'page_obj': page_obj})
