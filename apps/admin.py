from django.contrib import admin
from django.utils.safestring import mark_safe

from modeltranslation.admin import TranslationAdmin
from .forms import PostAdminForm
from .models import Category, ClassMMORPG, Post, PostShort, Author, Rating, RatingStar, Reviews





@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    """Категории"""
    list_display = ("name", "url")
    list_display_links = ("name",)


class ReviewInline(admin.TabularInline):
    """Отзывы на странице объявления"""
    model = Reviews
    extra = 1
    readonly_fields = ("name", "email")


class PostShotsInline(admin.TabularInline):
    model = PostShort
    extra = 1
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="100" height="110"')

    get_image.short_description = "Изображение"


@admin.register(Post)
class PostAdmin(TranslationAdmin):
    """объявления"""
    list_display = ("title", "category", "url", "draft")
    list_filter = ("category","class_MMORPG")
    search_fields = ("title", "category__name")
    inlines = [ReviewInline]
    save_on_top = True
    save_as = True
    list_editable = ("draft",)
    actions = ["publish", "unpublish"]
    form = PostAdminForm
    readonly_fields = ("get_image",)
    fieldsets = (
        (None, {
            "fields": (("title", "tagline"),)
        }),
        (None, {
            "fields": ("description", ("poster", "get_image"))
        }),
        (None, {

            "fields": (( "class_MMORPG", "category", 'author'),)
        }),
        ("Options", {
            "fields": (("url", "draft"),)
        }),
    )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.poster.url} width="100" height="110"')

    def unpublish(self, request, queryset):
        """Снять с публикации"""
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = "1 запись была обновлена"
        else:
            message_bit = f"{row_update} записей были обновлены"
        self.message_user(request, f"{message_bit}")

    def publish(self, request, queryset):
        """Опубликовать"""
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = "1 запись была обновлена"
        else:
            message_bit = f"{row_update} записей были обновлены"
        self.message_user(request, f"{message_bit}")

    publish.short_description = "Опубликовать"
    publish.allowed_permissions = ('change', )

    unpublish.short_description = "Снять с публикации"
    unpublish.allowed_permissions = ('change',)

    get_image.short_description = "Постер"


@admin.register(Reviews)
class ReviewAdmin(admin.ModelAdmin):
    """Отзывы к объявлению"""
    list_display = ("name", "email", "parent", "post", "id")
    readonly_fields = ("name", "email")


@admin.register(ClassMMORPG)
class ClassMMORPGAdmin(TranslationAdmin):
    """Классы"""
    list_display = ("name", "url")


@admin.register(Author)
class AuthorAdmin(TranslationAdmin):
    """Авторы"""
    list_display = ("name", "age", "get_image")
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60"')

    get_image.short_description = "Изображение"


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Рейтинг"""
    list_display = ("star", "post", "ip")


@admin.register(PostShort)
class PostShotsAdmin(TranslationAdmin):
    """Картинки из объявления"""
    list_display = ("title", "post", "get_image")
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60"')

    get_image.short_description = "Изображение"


admin.site.register(RatingStar)

admin.site.site_title = "Django BoardGAME"
admin.site.site_header = "Django BoardGAME"
