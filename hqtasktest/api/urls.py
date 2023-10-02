from django.urls import path
from . import api_views

app_name = 'api'


urlpatterns = [
    path('user/<int:pk>/lessons', api_views.LessonListView.as_view()),
    path('user/<int:pk>/products', api_views.UserProductsListView.as_view()),
    path('products/', api_views.ProductsListView.as_view())
]
