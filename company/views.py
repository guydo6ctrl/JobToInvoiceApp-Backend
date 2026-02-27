from rest_framework import viewsets, permissions, filters
from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from .models import BankDetails, CompanyDetails
from .serializers import BankDetailsSerializer, CompanyDetailsSerializer


class CompanyDetailsViewSet(viewsets.ModelViewSet):
    serializer_class = CompanyDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CompanyDetails.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        if hasattr(self.request.user, "company"):
            raise PermissionDenied("You already have a company profile.")
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.user != self.request.user:
            raise PermissionDenied("Cannot update another user's company.")
        serializer.save()


class BankDetailsViewSet(viewsets.ModelViewSet):
    serializer_class = BankDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return BankDetails.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.user != self.request.user:
            raise PermissionDenied("Cannot update another user's bank details.")
        serializer.save()

    def perform_create(self, serializer):

        serializer.save(user=self.request.user)
