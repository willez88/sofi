from django.urls import path

from .ajax import ComboUpdateView
from .views import Error403View, HomeView

app_name = 'base'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('error-403/', Error403View.as_view(), name='error_403'),

    path(
        'ajax/combo-update/', ComboUpdateView.as_view(),
        name='combo_update'
    ),
]
