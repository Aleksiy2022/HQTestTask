from .models import Product
from rest_framework import serializers


class ProductsListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = (
            'title',
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['statistics'] = {
            'users': instance.count_users,
            'viewed_lessons': instance.get_total_viewed_lesson(),
            'total_view_time': instance.get_total_view_time(),
            'users_ratio': instance.users_percent,
        }
        return data


class LessonSerializer(serializers.Serializer):
    title = serializers.CharField()
    viewed_status = serializers.BooleanField(source='viewed_lessons__view_status')
    view_time = serializers.IntegerField(source='viewed_lessons__view_time')


class UserProductsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = (
            'title',
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        product_title = data['title']
        data['lessons'] = []
        lessons = self.context.get('lessons')
        count_obj = len(lessons)
        for index in range(count_obj):
            if product_title == lessons[index]['products__title']:
                lesson_dict = {
                    'title': lessons[index]['title'],
                    'view_status': lessons[index]['viewed_lessons__view_status'],
                    'view_time': lessons[index]['viewed_lessons__view_time'],
                    'last_viewing': lessons[index]['viewed_lessons__last_viewing'],
                }
                data['lessons'].append(lesson_dict)
        return data
