from rest_framework.routers import DefaultRouter
from directory.api.views import UsersViewSet

router = DefaultRouter(
    trailing_slash=False,
)
router.register(
    'users/?', UsersViewSet, basename='users',
)
urlpatterns = router.urls
