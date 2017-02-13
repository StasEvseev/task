from django.conf.urls import url
from rest_framework.routers import SimpleRouter

from storage import views
from storage.views import image

router = SimpleRouter()
router.register(r'storage', views.MyViewSet, base_name='storage')

urlpatterns = router.urls

urlpatterns += [
    url(r'image/', image, name='image-proxy'),
]
