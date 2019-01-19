from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.views import generic
from django.urls import reverse_lazy, reverse
from .forms import CustomUserCreationForm, PostCreateForm, CommentCreateForm, PostEditForm
from .models import Post, CustomUser, Comment
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect
# from django.contrib.auth.decorators import login_required
# # views go here.
#
# @login_required
# def home(request):
#     return render(request, home.html, {})

class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    template_name = 'blog/signup.html'
    success_url = reverse_lazy('login')

@method_decorator(login_required(login_url='login'), name='dispatch')
class PostCreate(generic.CreateView):
    # model = Post
    # fields = ['post_text']
    form_class = PostCreateForm
    template_name = 'blog/postcreate.html'
    success_url = reverse_lazy('blog:home')
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

@login_required(login_url='login')
def commentcreate(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentCreateForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect('blog:home')
    else:
        form = CommentCreateForm()
    return render(request, 'blog/commentcreate.html', {'form': form})

class Home(generic.TemplateView):
    template_name = 'blog/home.html'
    # post_list = Post.objects.all()
    # poster = CustomUser.objects.get(pk=.user)
    # extra_context={'post_list': Post.objects.all()}
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_list'] = Post.objects.all()
        return context

@login_required(login_url='login')
def postsedited(request, current_post_pk):
    print(current_post_pk)
    return render(request, 'blog/postsedited.html', {'postpk':current_post_pk,'post_list':Post.objects.all()})

# class Profile(generic.DetailView):
#     model = CustomUser
#     template_name = 'blog/profile.html'
#     def get_queryset(self):
#         return self.request.user

@login_required(login_url='login')
def profile(request, username):
    user_req = get_object_or_404(CustomUser, username=username)
    return render(request, 'blog/profile.html', {'user_req':user_req})

@method_decorator(login_required(login_url='login'), name='dispatch')
class ProfileEdit(generic.UpdateView):
    model = CustomUser
    fields = ['first_name', 'last_name', 'email']
    template_name = 'blog/profile_edit.html'
    def get_object(self, queryset=None):
        obj = self.request.user
        return obj
    def get_success_url(self):
        return reverse('blog:home')

@login_required(login_url='login')
def follow(request):
    to_follow = CustomUser.objects.get(username = request.POST['followuser'])
    request.user.follows.add(to_follow)
    request.user.save()
    return render(request, 'blog/followed.html', {'userfollowed': to_follow})

@login_required(login_url='login')
def followedposts(request):
    return render(request, 'blog/followedusersposts.html', {'post_list':Post.objects.all()})

@login_required(login_url='login')
def postdelete(request, pk):
    post_to_delete = Post.objects.get(pk=pk)
    if request.user.pk is post_to_delete.user.pk:
        post_to_delete.is_deleted = True
        post_to_delete.save()
    return redirect('blog:home')

@login_required(login_url='login')
def postedit(request, pk):
    post_to_edit = get_object_or_404(Post, pk=pk)
    post_tosave = Post()
    post_tosave.post_text = post_to_edit.post_text
    post_tosave.is_before_edit = True
    post_tosave.user = post_to_edit.user
    post_tosave.pub_datetime = post_to_edit.pub_datetime
    post_tosave.current_post_pk = post_to_edit.pk
    if request.method == "POST":
        form = PostEditForm(request.POST, instance=post_to_edit)
        if form.is_valid():
            post_tosave.save()
            form.save()
            return redirect('blog:home')
    else:
        form = PostEditForm(instance=post_to_edit)
    return render(request, 'blog/post_edit.html', {'form': form, 'object':Post.objects.get(pk=pk)})
