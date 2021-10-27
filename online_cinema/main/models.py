from django.contrib.auth import get_user_model
from django.db import models
from model_utils import Choices
from django.contrib.contenttypes.fields import GenericRelation
from likes.models import Like

User = get_user_model()

class CreatedatModel(models.Model):
    
    """
    Нужен, чтобы не прописывать в каждом классе
    дату создания
    """

    created_at = models.DateTimeField(auto_now_add=True, null=True)

class ProductInfoMixin:
    """
    Хранит в себе общую информацию о продуктах
    """
    STATUS = Choices('Есть в наличии', 'Нет в наличии')
    COUNTRY = Choices('RUS', 'ENG', 'KGZ', 'DEU', 'EGY', 'KAZ', 'CHN', 'KOR', 'TUR',)
    GENRES = Choices(
        'аниме', 'боевик', 'вестерн', 'военный', 'детектив', 'документальный', 'драма', 'исторический', 'комедия', 'короткометражный', 'криминал', 'мелодрама', 'мультфильм', 'научный', 'приключения', 'семейный', 'триллер', 'ужасы', 'фантастика', 'фэнтези', 'эротика',
    )
    RATING = Choices(1,2,3,4,5,6,7,8,9,10)
 
class CinemaProduct(CreatedatModel, ProductInfoMixin, models.Model):

    title = models.CharField(max_length=50, unique=True)
    year = models.DecimalField(max_digits=5, decimal_places=2) 
    salesman = models.CharField(max_length=50)
    genre = models.CharField(choices=ProductInfoMixin.GENRES, max_length=25)
    image = models.ImageField(upload_to='images/cinema_images', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    country = models.CharField(choices=ProductInfoMixin.COUNTRY, max_length=25)
    likes = GenericRelation(Like, null=True, blank=True)

    def __str__(self):
        return self.title

    @property
    def total_likes(self):
        return self.likes.count()

class CinemaProductReview(CreatedatModel):
    cinema = models.ForeignKey(
        CinemaProduct, on_delete=models.CASCADE,
        related_name='cinema_reviews'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, 
        related_name='cinema_reviews',
        null=True
    )
    image = models.ImageField(
        upload_to='images/cinema_review',
        null=True, blank=True
    )
    text = models.TextField()
    rating = models.PositiveIntegerField(choices=ProductInfoMixin.RATING)

    def __str__(self) -> str:
        return str(self.author)