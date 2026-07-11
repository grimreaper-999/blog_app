from django.shortcuts import render ,redirect ,get_object_or_404
from django.http import JsonResponse
import random
from django.contrib.auth.decorators import login_required
from .models import Blog
# Create your views here.
@login_required
def home(view):
    request=view
    if 'feed_ids' not in request.session:
        all_ids =list(Blog.objects.values_list('id' ,flat=True))
        random.shuffle(all_ids)
        request.session['feed_ids']=all_ids
    is_ajax=(
        request.GET.get('ajax') =='1' or
        request.headers.get('X-Requested-With') == 'XMLHttpRequest' or
        request.META.get('HTTP_X_REQUESTED_WITH')== 'XMLHttpRequest'
    )

    if is_ajax:
        page= int(request.GET.get('page',1))
        per_page=10
        shuffled_ids =request.session.get('feed_ids',[])
        # print(f'fetching page{page}')
        # print(f'ids :{shuffled_ids}')
        start= (page-1)*per_page
        end=start + per_page
        batch_ids =shuffled_ids[start:end]
        posts = Blog.objects.filter(id__in= batch_ids)
        posts_by_id ={post.id:post for post in posts}
        ordered_posts = [posts_by_id[pid] for pid in batch_ids if pid in posts_by_id]
        data =[]
        for post in ordered_posts:
            author_str=post.author.username if post.author else 'Annonymous'
            date_str = post.created_at.strftime('%b %d ,%Y') if post.created_at else "Recently"
            data.append({
                'id':post.id,
                'title':post.title,
                'subtitle':post.subtitle,
                'content':post.content,
                'author':author_str,
                'date':date_str,

            })
        return JsonResponse({'posts':data ,'has_next':end < len(shuffled_ids)})
    else:
        all_ids=list(Blog.objects.values_list('id',flat=True))
        random.shuffle(all_ids)

        request.session['feed_ids']=all_ids
        initial_ids= all_ids[0:10]
        posts=Blog.objects.filter(id__in=initial_ids)
        posts_by_id ={post.id: post for post in posts}
        inittial_posts =[posts_by_id[pid] for pid in initial_ids if pid in posts_by_id]
        return render(request,'home.html' ,{'posts': inittial_posts})

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