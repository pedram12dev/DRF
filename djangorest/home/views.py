from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Person
from .serializers import PersonSerializer


class HomeView(APIView):
    def get(self , request):
        persons = Person.objects.all()
        serz_data = PersonSerializer(instance=persons , many=True)
        return Response(data=serz_data.data)