from rest_framework import status
from django.shortcuts import redirect
# from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
# from snippets.models import Snippet
# from snippets.serializers import SnippetSerializer
from .models import Advocate,Company
from .serializers import AdvocateSerializer,CompanySerializer
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
def endpoints(request):
    data =['/advocates','advocates/:username']
    return Response(data)

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def advocates_list(request):
    
    if request.method=='GET':
        query=request.GET.get('query')
        
        if query==None:
            query=''
            
        advocates = Advocate.objects.filter(
            Q(username__icontains=query) | Q(bio__icontains=query)
        )
        serializer=AdvocateSerializer(advocates,many=True)
        return Response(serializer.data)
    
    if request.method=='POST':

        advocate=Advocate.objects.create(
            username=request.data['username'],
            bio=request.data['bio']
        )
        serializer=AdvocateSerializer(advocate,many=False)
        return Response(serializer.data)
        



class AdvocateDetails(APIView):
    def get_object(self, username):
        try:
            return Advocate.objects.get(username=username)
        except Advocate.DoesNotExist:
            raise Response("Advocates does not exist")
    
    def get(self,request,username):
        advocate=self.get_object(username)
        serializer=AdvocateSerializer(advocate,many=False)
        return Response(serializer.data)
    
    def put(self,request, username):
        advocate=self.get_object(username)
        advocate.username=request.data['username']
        advocate.bio=request.data['bio']
        advocate.save()
        serializer=AdvocateSerializer(advocate,many=False)
        return Response(serializer.data)
    
    def delete(self,request,username):
        advocate=self.get_object(username)
        advocate.delete()
        return Response('User was deleted')
        
# @api_view(['GET','PUT','DELETE'])
# def advocate_details(request,username):
#     advocate=Advocate.objects.get(username=username)
    
#     if request.method =="GET":
        # serializer=AdvocateSerializer(advocate,many=False)
        # return Response(serializer.data)
#     if request.method =='PUT':
        # advocate.username=request.data['username']
        # advocate.bio=request.data['bio']
        # advocate.save()
        # serializer=AdvocateSerializer(advocate,many=False)
        # return Response(serializer.data)
    
#     if request.method =='DELETE':
        # advocate.delete()
        # return Response('User was deleted')


class CompaniesList(APIView):
    def get_object(self):
        try:
            return Company.objects.all()
        except Advocate.DoesNotExist:
            raise Response("Company does not exist")
        
    def get(self,request):
        company=self.get_object()
        serializer=CompanySerializer(company, many=True)
        return Response(serializer.data)
        