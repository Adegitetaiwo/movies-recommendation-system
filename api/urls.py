from django.urls import path, include
from rest_framework import routers
from .views import movieInputViewset, recommendModel

router = routers.DefaultRouter()
router.register('movies', movieInputViewset)

urlpatterns = [
    path('', include(router.urls)),
    path('recommend/', recommendModel)
]


# router = routers.DefaultRouter()
# router.register('language', views.languageView)

# urlpatterns = [
#     path('', include(router.urls))
# ]

