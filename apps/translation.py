from modeltranslation.translator import register, TranslationOptions
from .models import Category, Author, Post, ClassMMORPG, PostShort


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


@register(Author)
class AuthorTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(ClassMMORPG)
class GenreTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


@register(Post)
class PostTranslationOptions(TranslationOptions):
    fields = ('title', 'tagline', 'description', )


@register(PostShort)
class PostShotsTranslationOptions(TranslationOptions):
    fields = ('title', 'description')
