from django.urls import path
from . import views

urlpatterns = [
    path('', views.secrets, name='secrets'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('secrets/', views.secrets, name='secrets'),
    path('search/', views.search_secrets, name='search_secrets'),
    path('secret/<int:secret_id>/', views.secret_detail, name='secret_detail'),
    path('create/', views.create_secret, name='create_secret'),
    path('import/', views.import_secrets, name='import_secrets'),

    # Fixed versions
    path('fixed/search/', views.search_secrets_fixed, name='search_secrets_fixed'),
    path('fixed/secret/<int:secret_id>/', views.secret_detail_fixed, name='secret_detail_fixed'),
]