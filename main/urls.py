from django.conf.urls import url, include
from rest_framework import routers
from rest_framework.authtoken import views
import view

router = routers.DefaultRouter()
router.register(r'users', view.CmsUserViewSet)
router.register(r'events', view.EventViewSet)
router.register(r'songs', view.SongViewSet)
router.register(r'likes', view.LikeViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', views.obtain_auth_token),
]