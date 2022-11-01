from email.policy import HTTP

from django.shortcuts import render
import datetime

from rest_framework import viewsets
from django.contrib.auth.models import User
from library.models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework import permissions, authentication
from library.tasks import *

from datetime import date, timedelta


from library.serializers import BookSerializer, UserRegistrationSerializer, IssueSerializer

# Create your views here.

"""CRUD for Book """
class BookViewSet(viewsets.ModelViewSet):

    permission_classes = [permissions.IsAuthenticated]

    serializer_class = BookSerializer
    queryset = Book.objects.all()
    model = Book

""" Registration """
class UserRegistrationView(APIView):

    serializer_class = UserRegistrationSerializer

    def get(self, request, *args, **kwargs):
        try:
            user_list = User.objects.all()
            serializer = self.serializer_class(user_list, many=True)
            
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            print("\nException Occured", error)

    def post(self, request, format=None):
        
            response = {'status':status.HTTP_400_BAD_REQUEST, 'message': "Registration Failed"}
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid(raise_exception=False):
                user = serializer.save()
                response["status"] = status.HTTP_201_CREATED
                response["data"] = serializer.data
                response["message"] = 'Registration Successfull'
                return Response(response, status=status.HTTP_201_CREATED)
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
      
""" Book Issue/Return """

class IssueBookView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    serializer_class = IssueSerializer

    def get(self, request, *args, **kwargs):
        try:
            issued_list = IssueBook.objects.all()
            serializer = self.serializer_class(issued_list, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            print("\nException Occured", error)

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            response = {'status':status.HTTP_400_BAD_REQUEST, 'message': "Book issuance Failed"}

            """ fetch email for send mail """
            id = request.data['user']
            send_mail = User.objects.get(id=id)
            e_mail = send_mail.email

            """ fetch bookname and author """
            book_id = request.data['book']
            books = Book.objects.get(id=book_id)
            book = books.title
            author = books.author

            date = request.data['issue_date']

            if serializer.is_valid():

                serializer.save()

                response["status"] = status.HTTP_200_OK
                response["data"] = serializer.data
                response["message"] = 'Book Issued Successfully'

                message = 'Your Book  is issued successfully...! \n\n Book Name:' f"{book} \n\n Author: {author} \n\n Issue date: {date}\n \n Kindly return the same in 7 days. \n \n Happy Reading..!"

                send_issue_mail.delay(e_mail, message)

                return Response(response, status=status.HTTP_200_OK)
            else:
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            print('Exception Occured',e)


    def put(self, request, *args, **kwargs):
        try:
    
            id = kwargs.get("id")
            print(id)
            instance = IssueBook.objects.get(id=id)
            serializer = IssueSerializer(data=request.data)

            """ fetch email for send mail """
            id = request.data['user']
            send_mail = User.objects.get(id=id)
            e_mail = send_mail.email

            """ fetch bookname and author """
            book_id = request.data['book']
            books = Book.objects.get(id=book_id)
            book = books.title
            author = books.author

            date = request.data['return_date']

            if serializer.is_valid():

                status = serializer.validated_data.get("status")

                return_date = serializer.validated_data.get("return_date")

                instance.status = status

                instance.return_date = return_date

                instance.save()

                message = 'You have returned the Book..! \n\n Book Name:'  f"{book} \n\n Author: {author} \n\n Book Return Date: {date}. \n \n Thank you.!"

                send_return_mail.delay(e_mail, message)
                
                return Response({'Book Returned Successfully'})
            else:
                return Response({'Book Return Failed'} )

        except Exception as e:
            print('\n Exception Occured',e)

      
"""Fetch Issue/Return Book Details """ 

class BookDetails(APIView):

    permission_classes = [permissions.IsAuthenticated]

    serializer_class = IssueSerializer

    def get(self, request, *args, **kwargs):
        
            try:
                response = {'status':status.HTTP_400_BAD_REQUEST, 'message': "Book Details Not Found"}
                id = kwargs.get('id')
                issued_list = IssueBook.objects.get(id = id)
                serializer = self.serializer_class(issued_list)
                response["status"] = status.HTTP_200_OK
                response["data"] = serializer.data
                response["message"] = 'Book Details Fetched Succesfully'
                return Response(response, status=status.HTTP_200_OK)
            except Exception:
                return Response(response,status=status.HTTP_400_BAD_REQUEST)


""" Search """

class SearchView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):

        try:

                response = {'status':status.HTTP_400_BAD_REQUEST, 'message': "Book not available"}

                title = request.data['name']
                book_obj = Book.objects.filter(title__icontains=title)
                # print(instance)
                book_list = []
                for i in book_obj:
                    book = i.title
                
                    book_list.append(book)
                    
                    response["status"] = status.HTTP_200_OK
                    response["data"] = book_list
                    response["message"] = 'Book is Available'
                    print(book_list)

                return Response(response)
                
                # else:
                #     return Response(response, status=status.HTTP_400_BAD_REQUEST)


        except Exception as e:
            print('Exception Occured',e)

        
