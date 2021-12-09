from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers

from recettela.services.spoonacular import reverse_recipe
from recettela.api import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

urlpatterns = [
    # path('foods/', views.food_list),
    # url('foods/', views.ListCreateFoodView.as_view()),
    path('foods/', views.FoodList.as_view()),
    path('foods/<int:pk>/', views.FoodDetail.as_view()),
    #path('foods/<int:pk>/', views.food_detail),
    path('', include(router.urls)),
    url('reverse_recipe/', reverse_recipe, name='reverse_recipe'),
]
