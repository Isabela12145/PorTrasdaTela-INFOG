from django.contrib import admin
from django.urls import path
from app import views
from app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.index, name="index"),

    path('alerta/', views.alerta, name="alerta"),
    path('diario/', views.diario, name="diario"),
    path('ranking/', views.ranking, name="ranking"),
    path('recompensa/', views.recompensa, name="recompensa"),
    path('profissionais/', views.profissionais, name="profissionais"),
        
    # Autenticação(Auth)
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),

    # Logout
    path('logout/', logout_view, name='logout'),
]
