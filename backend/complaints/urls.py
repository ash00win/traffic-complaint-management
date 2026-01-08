from django.urls import path
from .views import ComplaintListCreateView, ComplaintStatusUpdateView

urlpatterns = [
    path('', ComplaintListCreateView.as_view(), name='complaint-list-create'),
    path('<int:pk>/status/', ComplaintStatusUpdateView.as_view(), name='complaint-status-update'),
]
