from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from chamados import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path(
        'login/',
        views.LoginUsuarioView.as_view(),
        name='login'
    ),

    path(
        'logout/',
        auth_views.LogoutView.as_view(
            next_page='/login/'
        ),
        name='logout'
    ),

    path('', include('chamados.urls')),
]