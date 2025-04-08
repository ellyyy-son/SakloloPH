from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, PostImage
from .forms import PostForm, PostImageForm
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404, render


def home(request):
    return render(request, 'landing_page.html')

def request_view(request):
    user_posts = Post.objects.filter(user=request.user).order_by('-date')
    return render(request, 'requests.html', {'posts': user_posts})

def contact_view(request):
    return render(request, 'contact.html')

class PostListView(ListView):
    model = Post
    template_name = 'post_list.html'
    paginate_by = 5  
    ordering = ['-date']  


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'post_detail.html'
    redirect_field_name = ''


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post_create.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)

        for uploaded_file in self.request.FILES.getlist('image'):
            PostImage.objects.create(
                post=self.object,
                image=uploaded_file
            )

        return response

    def get_success_url(self):
        return reverse_lazy('report:post_list')


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = "post_update.html"
    form_class = PostForm

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.get_object().pk})

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['post_image_form'] = PostImageForm()
        return ctx

    def post(self, request, *args, **kwargs):
        current_post = self.get_object()
        post_form = PostForm(request.POST, request.FILES, instance=current_post)
        
        if post_form.is_valid():
            post_form.save()
            
            images = request.FILES.getlist('image') 
            for image in images:
                PostImage.objects.create(post=current_post, image=image)
            
            return redirect(self.get_success_url())
        else:
            ctx = self.get_context_data(**kwargs)
            ctx['form'] = post_form
            return self.render_to_response(ctx)


def upvote_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.upvotes += 1
    post.save()
    return redirect(post.get_absolute_url())

def downvote_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.downvotes += 1
    post.save()
    return redirect(post.get_absolute_url())
