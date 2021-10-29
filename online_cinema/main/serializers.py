# from model_utils import fields
# import requests
# from typing_extensions import Required
from rest_framework import serializers
from likes.serializers import FanSerializer

from main.models import *
from rest_framework import serializers
from main.models import CinemaProduct
from likes import services as likes_services

class CinemaProductSerializer(serializers.ModelSerializer):
    is_fan = serializers.SerializerMethodField()
    class Meta:
        model = CinemaProduct
        fields = (
            'id',
            'title',
            'year',
            'salesman',
            'genre',
            'image',
            'country',
            'description',
            'price',
            'file',
            'is_fan',
            'total_likes',
        )

    def get_is_fan(self, obj) -> bool:
        request = self.context.get('request')
        if request:
            return likes_services.is_fan(obj, request.user)

    def to_representation(self, instance):
        representation = super(
            CinemaProductSerializer, self
        ).to_representation(instance)
        representation['comments'] = CinemaCommentSerializer(
            CinemaProductComment.objects.filter(cinema=instance.id),
            many=True
        ).data

        #
        representation['favorite'] = CinemaFavoriteSerializer(
            CinemaProductFavorite.objects.filter(cinema=instance.id),
            many=True
        ).data
        #

        matches = CinemaProduct.objects.filter(title=instance.genre).values()
        match_show_info = {}
        for match in matches:
            match_show_info.update(
            {
                "title": match["title"],
                "description": match["description"],
                "price": match["price"],
                "image": match["image"],
            }
            )
        
        representation['match'] = match_show_info

        if representation.get('status') == "Есть в наличии":
            # payload = {
            #     'product_name': representation.get("title"),
            #     'product_price': float(representation.get("price")),
            #     }
            # r = requests.post(
            #     'http://127.0.0.1:8000/api/v1/cart_items/',
            #     data=payload)  
            representation['add_to_cart'] = 'http://127.0.0.1:8000/api/v1/cart_items/'

        # Подсчет суммы оценок и вывод среднего арифметического
        # (Средняя оценка)
        rating_list = []
        for comment in representation['comments']:
            rating_list.append(comment['rating'])
        # Если нет отзывов
        try:
            representation['cinema_rating'] = round(sum(rating_list) / len(rating_list), 2)
        except ZeroDivisionError:
            representation['cinema_rating'] = None
        return representation
    
###############################



###################################


class ReviewMixin:
    def get_cinema_title(self, cinema_review):
        title = cinema_review.cinema.title
        return title

class CinemaCommentSerializer(ReviewMixin, serializers.ModelSerializer):
    class Meta:
        model = CinemaProductComment
        fields = (
            # "id",
            "author",
            "cinema",
            "cinema_title",
            "text",
            "image",
            "rating",
            "created_at",
        )

    cinema_title = serializers.SerializerMethodField("get_cinema_title")

    def create(self, validated_data):
        request = self.context.get('request')
        author_email = request.user
        comment_info = CinemaProductComment.objects.create(author=author_email, **validated_data)
        return comment_info
        
    def validate_product(self, cinema):
        request = self.context.get('request')
        
        if cinema.cinema_reviews.filter(
            author=request.user
        ).exists():
            raise serializers.ValidationError(
                "Вы уже оставляли отзыв на данный продукт"
                )
        return cinema


########################

class CinemaFavoriteSerializer(ReviewMixin, serializers.ModelSerializer):
    class Meta:
        model = CinemaProductFavorite
        fields = (
            # "id",
            "author",
            "cinema",
            "cinema_title",
            "created_at",
        )

    cinema_title = serializers.SerializerMethodField("get_cinema_title")

    def create(self, validated_data):
        request = self.context.get('request')
        author_email = request.user
        favorite_info = CinemaProductFavorite.objects.create(author=author_email, **validated_data)
        return favorite_info
        
    def validate_product(self, cinema):
        request = self.context.get('request')
        
        if cinema.cinema_reviews.filter(
            author=request.user
        ).exists():
            raise serializers.ValidationError(
                "Вы уже добавили в избранное"
                )
        return cinema


