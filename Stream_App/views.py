from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from .forms import CommentForm, VideoForm, CategoryForm
import uuid
from .models import Comment, Video, Category
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, DeleteView, TemplateView, ListView, DetailView, View

# Create your views here.


def home(request):
    videos = Video.objects.all()
    if request.method == 'GET':
        search = request.GET.get('search', '')
        result = Video.objects.filter(video_title__icontains=search)
    return render(request, 'Stream_App/home.html', context={'videos': videos, 'search': search, 'result': result})


def category_list(request, pk):
    category_info = Category.objects.get(pk=pk)
    category_videos = Video.objects.filter(category=category_info)
    return render(request, 'Stream_App/category_list.html', context={'videos': category_videos})


@login_required
def upload_videos(request):
    form = VideoForm()
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            title = video.video_title
            video.user = request.user
            video.slug = title.replace(' ', '-') + str(uuid.uuid4())
            video.save()
            return HttpResponseRedirect(reverse('home'))
    return render(request, 'Stream_App/upload_videos.html', context={'form': form})


def edit_videos(request):
    return render(request, 'Stream_App/home.html')


@login_required
def details_videos(request, slug):
    video = Video.objects.get(slug=slug)
    comment_form = CommentForm()
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.video = video
            comment.save()
            return HttpResponseRedirect(reverse('Stream_App:details_videos', kwargs={'slug': slug}))
    return render(request, 'Stream_App/video_details.html', context={'video': video, 'form': comment_form})


class MyVideos(LoginRequiredMixin, TemplateView):
    template_name = "Stream_App/myvideos.html"


class Delete_Video(LoginRequiredMixin, DeleteView):
    model = Video
    template_name = "Stream_App/delete_video.html"
    success_url = reverse_lazy('Stream_App:my_videos')


@login_required
def edit_video(request, slug):
    video = Video.objects.get(slug=slug)
    form = VideoForm(instance=video)
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES, instance=video)
        if form.is_valid():
            form.save()
            form = VideoForm(instance=video)
            return HttpResponseRedirect(reverse('Stream_App:my_videos'))
    return render(request, 'Stream_App/update_video.html', context={'form': form, 'edit': True})


class add_category(LoginRequiredMixin, CreateView):
    model = Category
    template_name = 'Stream_App/categoryform.html'
    fields = ['name', 'image']

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse('Stream_App:upload_videos'))


def categories(request):
    categories = Category.objects.all()
    return render(request, 'Stream_App/categories.html', context={'categories': categories})
