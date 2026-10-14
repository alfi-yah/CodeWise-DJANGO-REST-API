from django.shortcuts import render
from Repository.models import Questions
from Repository.serializers import QuestionSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.

class QuestionListCreateView(APIView):
	def get(self, request):
		qs = Questions.objects.all() # Collection of questions

		# many = True means tells the serializer that the input contains mutliple objects
		serializer_instance = QuestionSerializer(qs, many=True) 

		# Return the serilaized data as a response
		return Response(serializer_instance.data)


	def post(self, request):
		form_data = request.data   										# form_data dictionary --> python native type
		serializer_instance = QuestionSerializer(data=form_data)  		# creates a serializer instance and is passed to the serializer which we created
		if serializer_instance.is_valid():    							# checks if the data is valid according to the seerializer's validation rules
			actual_data = serializer_instance.validated_data  			# get the validated data from the serializer
			Questions.objects.create(**actual_data)   					# creates the table by using keyword args
			return Response(data= serializer_instance.data)  			# returns the data
		else:
			return Response(data=serializer_instance.errors) 			# if the data isn't valid it returns the error

class QuestionRetriveUpdateDeleteView(APIView):
	def get(self, request, pk):        					# pk is the primary key of the question to retrieve
		qs = Questions.objects.get(id=pk)				# get the question object with the given primary key
		serializer_instance = QuestionSerializer(qs) 	# serialize the question object
		return Response(data=serializer_instance.data) 	# return the serialized data as a response

	def put(self, request, pk):   									# pk is the primary key of the question to update
		form_data = request.data  
		serializer_instance = QuestionSerializer(data=form_data) 	# creates serializer instance wth form data
		if serializer_instance.is_valid():   						# checks if the data is valid according to the serializer's validation rules
			actual_data = serializer_instance.validated_data

			#modelname.objects.filter(id).update(filed=value)
			Questions.objects.filter(id=pk).update(**actual_data) 	# updates the question object with the given primary key
			return Response(data=serializer_instance.data)			# resturn the serialized data as a Response
		else:
			return Response(data=serializer_instance.errors)		# returns the validation errors as response
		