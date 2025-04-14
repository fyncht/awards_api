from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import ProfileSerializer


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = (JWTAuthentication,)

    def get(self, request):
        # user = request.user
        serializer = ProfileSerializer(request.user)
        # return Response({
        #     "username": user.username,
        #     "id": user.id,
        #     "is_authenticated": user.is_authenticated,
        #     "auth_header": request.META.get('HTTP_AUTHORIZATION'),
        # })
        return Response(serializer.data)
