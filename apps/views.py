from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
from django.views.generic.base import View


from .models import Post, Category, Author, ClassMMORPG, Rating, Reviews
from .forms import ReviewForm, RatingForm





class GenreСategory:
    """Жанры объявлений"""

    def get_ClassMMORPG(self):
        return ClassMMORPG.objects.all()

    def get_category(self):
        return Category.objects.all()

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class PostsView(GenreСategory, ListView):
    """Список объявлений"""
    model = Post
    queryset = Post.objects.filter(draft=False)
    paginate_by = 10



class PostDetailView(GenreСategory, DetailView):
    """Полное описание объявления"""
    model = Post
    queryset = Post.objects.filter(draft=False)
    slug_field = "url"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["star_form"] = RatingForm()
        context["form"] = ReviewForm()
        return context


class AddReview(View):
    """Отзывы"""

    def post(self, request, pk):
        form = ReviewForm(request.POST)
        movie = Post.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get("parent", None):
                form.parent_id = int(request.POST.get("parent"))
            form.movie = movie
            form.save()
        return redirect(movie.get_absolute_url())


class AuthorView(GenreСategory, DetailView):
    """Вывод информации об авторе"""
    model = Author
    template_name = 'apps/author.html'
    slug_field = "name"


class FilterPostsView(GenreСategory, ListView):
    """Фильтр объявлений"""
    paginate_by = 5

    def get_queryset(self):
        queryset = Post.objects.filter(
            Q(category__in=self.request.GET.getlist("category")) |
            Q(class_MMORPG__in=self.request.GET.getlist("class_MMORPG"))
        ).distinct()
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["year"] = ''.join([f"year={x}&" for x in self.request.GET.getlist("year")])
        context["genre"] = ''.join([f"genre={x}&" for x in self.request.GET.getlist("genre")])
        return context


class JsonFilterMovPostView(ListView):
    """Фильтр объявлений в json"""

    def get_queryset(self):
        queryset = Post.objects.filter(
            Q(category__in=self.request.GET.getlist("category")) |
            Q(class_MMORPG__in=self.request.GET.getlist("class_MMORPG"))
        ).distinct().values("title", "tagline", "url", "poster")
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = list(self.get_queryset())
        return JsonResponse({"apps": queryset}, safe=False)


class AddStarRating(View):
    """Добавление рейтинга объявлению"""

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                ip=self.get_client_ip(request),
                movie_id=int(request.POST.get("movie")),
                defaults={'star_id': int(request.POST.get("star"))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)


class Search(ListView):
    """Поиск фильмов"""
    paginate_by = 3

    def get_queryset(self):
        return Post.objects.filter(title__icontains=self.request.GET.get("q"))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = f'q={self.request.GET.get("q")}&'
        return context
