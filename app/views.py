from django.shortcuts import render ,redirect ,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Blog
# Create your views here.
@login_required
def home(request):
    return render(request,'home.html')
@login_required
def create(request):
    if request.method =="POST":
        user = request.user
        title =request.POST.get('title')
        subtitle= request.POST.get('excerpt')
        content =request.POST.get('content')
        Blog.objects.create(
            author=user,
            title=title,
            subtitle=subtitle,
            content=content
        )
        return redirect('home_page')

    return render(request,'create.html')


@login_required
def dashboard(request):
    user =request.user
    post =Blog.objects.filter(author=user)
    return render(request,'dashbord.html',{'posts':post})


@login_required
def edit_post(request,pk):
    blog =get_object_or_404(Blog,pk=pk)
    if blog.author!=request.user:
        return redirect('home_page')
    if request.method=="POST":
        blog.title=request.POST.get('title')
        blog.subtitle=request.POST.get('excerpt')
        blog.content= request.POST.get('content')
        blog.save()

        return redirect('profile')
    
    return render(request,"edit.html",{'blog':blog})


@login_required
def delete_blog(request,pk):
    blog =get_object_or_404(Blog,pk=pk)
    if blog.author!=request.user:
        return redirect('home_page')
    if request.method =="POST":
        blog.delete()
    return redirect('profile')