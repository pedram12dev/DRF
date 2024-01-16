from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Person, Question, Answer
from .serializers import PersonSerializer, QuestionSerializer, AnswerSerializer


class HomeView(APIView):
    def get(self, request):
        persons = Person.objects.all()
        serz_data = PersonSerializer(instance=persons, many=True)
        return Response(data=serz_data.data)


class QuestionView(APIView):
    def get(self, request):
        questions = Question.objects.all()
        serz_data = QuestionSerializer(instance=questions, many=True).data
        return Response(data=serz_data)

    def post(self, request):
        serz_data = QuestionSerializer(data=request.data)
        if serz_data.is_valid():
            serz_data.save()
            return Response(serz_data.data)
        return Response(serz_data.errors)

    def put(self, request, pk):
        question = Question.objects.get(pk=pk)
        serz_data = QuestionSerializer(instance=question , data=request.data , partial=True)
        if serz_data.is_valid():
            serz_data.save()
            return Response(serz_data.data)
        return Response(serz_data.errors)

    def delete(self, request, pk):
        question = Question.objects.get(pk=pk)
        question.delete()
        return Response({'message': 'question is deleted'})
