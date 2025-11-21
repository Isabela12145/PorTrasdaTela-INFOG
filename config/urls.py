from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.index, name="index"),
    path('login/', views.login_page, name="login"),
    path('login_user/', views.login_user, name="login_user"),
    path('logout/', views.logout_user, name="logout"),

    # páginas internas
    path('alerta/', views.alerta, name="alerta"),
    path('diario/', views.diario, name="diario"),
    path('ranking/', views.ranking, name="ranking"),
    path('recompensa/', views.recompensa, name="recompensa"),
    path('profissionais/', views.profissionais, name="profissionais"),
]
