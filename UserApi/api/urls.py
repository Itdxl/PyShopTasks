from django.urls import path
from .views import RegisterView, LoginView, ProfileView, TokenCheckView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('me/', ProfileView.as_view(), name='login'),
    path('check/', TokenCheckView.as_view(), name='token'),

]
