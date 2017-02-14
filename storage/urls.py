from rest_framework.routers import SimpleRouter

from storage import views

router = SimpleRouter()
router.register(r'storage', views.StorageViewSet, base_name='storage')

urlpatterns = router.urls
