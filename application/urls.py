from django.urls import path
from . import views

# Application namespace for URL reversing
app_name = 'application'

# URL patterns for the application
urlpatterns = [
    # Root URL maps to the index view
    # This is the main (and only) page of our application
    path('', views.index, name='index'),
    
    # Additional URL patterns can be added here as the application grows
    # For example:
    # path('history/', views.history, name='history'),
    # path('settings/', views.settings, name='settings'),
]
