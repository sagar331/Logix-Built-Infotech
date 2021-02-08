from rest_framework.routers import DefaultRouter
from registerapp import views
router = DefaultRouter()
router.register(r'register', views.RegisterView,basename='create')
router.register(r'login', views.LoginView,basename='login')
router.register(r'job', views.JobViewSet,basename='login')
urlpatterns = router.urls