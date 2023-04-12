import json
from django.db import connection
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class UserRegistration(APIView):

    def post(self, request):
        try:
            request_data = json.loads(request.body)
            first_name = request_data.get("first_name")
            last_name = request_data.get("last_name")
            username = request_data.get("username")
            password = request_data.get("password")
            email = request_data.get("email")
            with connection.cursor() as cursor: # connection.cursor() --- to get cursor object
                cursor.execute( # to execute sql
                    "INSERT INTO user_table(first_name, last_name, username, password,email) VALUES (%s, %s, %s, %s,%s)",
                    (first_name, last_name, username, password,email))
                cursor.execute("select * from user_table WHERE first_name=%s", [first_name])
                field_list = ['id', 'first_name', 'last_name','username', 'password','email']
                registered_data = {field_list[i]: row for i, row in enumerate(cursor.fetchone())}
                        #Enumerate() method adds a counter to an iterable and returns it in a form of enumerating object.

                return Response({"message": "Registration completed", "status": 200, "data": registered_data},
                                status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": e.args[0], "status": 400, "data": {}},
                            status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        try:
            cursor = connection.cursor()
            cursor.execute("select * from user_table")
            retrieved_data = [dict(zip([col[0] for col in cursor.description], row)) for row in cursor.fetchall()]
            a=[1,2,3]
            b=[4,5,6]
            print(list(zip(a,b)))
            # zip takes iterables as argument and matches one with the other
# fetchall() returns all the rows of a query result. It returns all the rows as a list of tuples.
#  An empty list is returned if there is no record to fetch.

            return Response({"message": "user list displayed", "status": 200, "data": retrieved_data},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": e.args[0], "status": 400, "data": {}})

    def put(self,request):
        try:
            request_data = json.loads(request.body)
            first_name = request_data.get("first_name")
            last_name = request_data.get("last_name")
            username = request_data.get("username")
            password = request_data.get("password")
            email = request_data.get("email")
            user_id=request_data.get('id')
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE user_table SET first_name=%s, last_name=%s, username=%s, password=%s, email=%s where id=%s",
                    [first_name, last_name, username, password, email, user_id])
                cursor.execute("select * from user_table WHERE first_name=%s", [first_name])
                field_list = ['id','first_name', 'last_name', 'username', 'password', 'email']
                registered_data = {field_list[i]: row for i, row in enumerate(cursor.fetchone())}
                #  fetchone() method returns a single record or None if no more rows are available.
                return Response({"message": "user updated", "status": 200, "data": registered_data},
                        status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response({"message": e.args[0], "status": 400, "data": {}},
                        status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request):
        try:

            request_data = json.loads(request.body)
            user_id = request_data.get("user_id")
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM user_table WHERE id=%s", [user_id])
                return Response({"message": "user deleted", "status": 200, "data": {}},
                                    status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response({"message": e.args[0], "status": 400, "data": {}},
                        status=status.HTTP_400_BAD_REQUEST)