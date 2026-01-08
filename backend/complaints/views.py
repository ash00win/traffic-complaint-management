from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Complaint
from .serializers import ComplaintSerializer
from .permissions import IsPoliceOrAdmin


class ComplaintListCreateView(generics.ListCreateAPIView):
    serializer_class = ComplaintSerializer
    permission_classes = [permissions.IsAuthenticated]

    # STEP 18 additions
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status']
    search_fields = ['title', 'location']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        user = self.request.user

        # Police/Admin see all complaints
        if user.role in ['police', 'admin']:
            return Complaint.objects.all()

        # Citizens see only their complaints
        return Complaint.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .permissions import IsPoliceOrAdmin

class ComplaintStatusUpdateView(APIView):
    permission_classes = [IsPoliceOrAdmin]

    def patch(self, request, pk):
        try:
            complaint = Complaint.objects.get(pk=pk)
        except Complaint.DoesNotExist:
            return Response(
                {"error": "Complaint not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        new_status = request.data.get('status')

        if new_status not in ['pending', 'in_progress', 'resolved', 'rejected']:
            return Response(
                {"error": "Invalid status"},
                status=status.HTTP_400_BAD_REQUEST
            )

        complaint.status = new_status
        complaint.save()

        return Response(
            {"message": "Status updated successfully"},
            status=status.HTTP_200_OK
        )
