from django.contrib.auth.models import User
from .models import Product, Lesson
from rest_framework import views
from rest_framework.response import Response
from rest_framework.request import Request
from .serializers import LessonSerializer, ProductsListSerializer, UserProductsSerializer
from django.db.models import Count


class LessonListView(views.APIView):
    """
    Вывод списка всех уроков по всем продуктам к которым пользователь имеет доступ.
    """

    def get(self, request: Request, pk: int) -> Response:
        lessons = (
            Lesson.objects.
            filter(viewed_lessons__user=pk, products__users=pk).
            values('title', 'viewed_lessons__view_status', 'viewed_lessons__view_time', ).
            distinct()
        )
        serializer = LessonSerializer(lessons, many=True)
        return Response(serializer.data)


class UserProductsListView(views.APIView):
    """
    Выводин список уроков по конкретному продукту к которому пользователь имеет доступ.
    """

    def get(self, request: Request, pk: int) -> Response:
        products = Product.objects.filter(users=pk)
        lessons = (
            Lesson.objects.
            filter(viewed_lessons__user=pk, products__users=pk).
            values(
                'products__title', 'title', 'viewed_lessons__view_status',
                'viewed_lessons__view_time', 'viewed_lessons__last_viewing'
            ).
            distinct()
        )
        context = {'lessons': lessons}
        serializer = UserProductsSerializer(products, context=context, many=True)
        return Response(serializer.data)


class ProductsListView(views.APIView):
    """
    Вывод списка всех продуктов на платформе и статистики по каждому продукту.
    """

    def get(self, request: Request) -> Response:
        total_users = User.objects.all().count()
        products = (
            Product.objects.
            prefetch_related('product').
            annotate(
                count_users=Count('users', distinct=True),
                users_percent=(Count('users', distinct=True) / float(total_users) * 100),
            )
        )
        serializer = ProductsListSerializer(products, many=True)
        return Response(serializer.data)
