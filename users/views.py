from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from users.serializers import UserSerializer, UserCreateSerializer, RoleAssignSerializer
from users.permissions import IsAdminOrSelf
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.template.loader import render_to_string
from django.http import FileResponse
from pyhtml2pdf import converter
import os
import uuid

User = get_user_model()

class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    authentication_classes = [JWTAuthentication]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserCreateSerializer
        return UserSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAdminUser()]

        if self.request.method == 'POST':
            try:
                is_staff = str(self.request.data.get('is_staff', False)).lower() in ['true', '1']
            except Exception:
                is_staff = False

            if is_staff:
                return [permissions.AllowAny()]
            else:
                return [permissions.IsAuthenticated(), permissions.IsAdminUser()]

        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save()


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrSelf]

    def get_object(self):
        
        obj = super().get_object()
        self.check_object_permissions(self.request, obj)
        return obj


class ProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class RoleAssignView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = RoleAssignSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PyHTML2PDFView(APIView):
    def get(self, request, format=None):
        name = request.GET.get("name", "Guest")

        # Render HTML to string
        html_content = render_to_string("sample_template.html", {"name": name})

        # Write the HTML to a temporary file
        html_filename = f"/tmp/{uuid.uuid4()}.html"
        pdf_filename = f"/tmp/{uuid.uuid4()}.pdf"

        with open(html_filename, "w", encoding="utf-8") as f:
            f.write(html_content)

        # Convert HTML to PDF
        converter.convert(f"file://{html_filename}", pdf_filename)

        # Serve the PDF file as response
        response = FileResponse(open(pdf_filename, "rb"), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="report.pdf"'

        # Clean up (optional in production)
        os.remove(html_filename)

        return response
