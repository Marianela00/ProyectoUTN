from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import status as HTTPStatus
from home.models import Carrera, Materia
from .serializers import CarreraSerializer, MateriaSerializer
from django.http import Http404

class CarreraView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def post(self, request):
        serializer = CarreraSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data={
                **serializer.errors,
                'success': False
            }, status=HTTPStatus.BAD_REQUEST)
        serializer.save()
        return Response(data={
            'message': 'Registro creado.',
            'success': True
        }, status=HTTPStatus.OK)

    def get(self, request, pk=None):
        if not pk:
            return Response({
                'data': [CarreraSerializer(instance=obj).data for obj in Carrera.objects.all()],
                'success': True
            }, status=HTTPStatus.OK)
        try:
            obj = get_object_or_404(Carrera, pk=pk)
        except Http404:
            return Response(data={
                'message': 'Objeto con la clave primaria proporcionada no encontrado.',
                'success': False
            }, status=HTTPStatus.NOT_FOUND)
        return Response({
            'data': CarreraSerializer(instance=obj).data,
            'success': True
        }, status=HTTPStatus.OK)

    def put(self, request, pk):
        try:
            obj = get_object_or_404(Carrera, pk=pk)
        except Http404:
            return Response(data={
                'message': 'Objeto con la clave primaria proporcionada no encontrado.',
                'success': False
            }, status=HTTPStatus.NOT_FOUND)
        serializer = CarreraSerializer(instance=obj, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(data={
                **serializer.errors,
                'success': False
            }, status=HTTPStatus.BAD_REQUEST)
        serializer.save()
        return Response(data={
            'message': 'Registro actualizado.',
            'success': True
        }, status=HTTPStatus.OK)

    def delete(self, request, pk):
        try:
            obj = get_object_or_404(Carrera, pk=pk)
        except Http404:
            return Response(data={
                'message': 'Objeto con la clave primaria proporcionada no encontrado.',
                'success': False
            }, status=HTTPStatus.NOT_FOUND)
        obj.delete()
        return Response(data={
            'message': 'Registro eliminado.',
            'success': True
        }, status=HTTPStatus.OK)

class MateriaView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def post(self, request):
        serializer = MateriaSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data={
                **serializer.errors,
                'success': False
            }, status=HTTPStatus.BAD_REQUEST)
        serializer.save()
        return Response(data={
            'message': 'Registro creado.',
            'success': True
        }, status=HTTPStatus.OK)

    def get(self, request, pk=None):
        if not pk:
            return Response({
                'data': [MateriaSerializer(instance=obj).data for obj in Materia.objects.all()],
                'success': True
            }, status=HTTPStatus.OK)
        try:
            obj = get_object_or_404(Materia, pk=pk)
        except Http404:
            return Response(data={
                'message': 'Objeto con la clave primaria proporcionada no encontrado.',
                'success': False
            }, status=HTTPStatus.NOT_FOUND)
        return Response({
            'data': MateriaSerializer(instance=obj).data,
            'success': True
        }, status=HTTPStatus.OK)

    def put(self, request, pk):
        try:
            obj = get_object_or_404(Materia, pk=pk)
        except Http404:
            return Response(data={
                'message': 'Objeto con la clave primaria proporcionada no encontrado.',
                'success': False
            }, status=HTTPStatus.NOT_FOUND)
        serializer = MateriaSerializer(instance=obj, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(data={
                **serializer.errors,
                'success': False
            }, status=HTTPStatus.BAD_REQUEST)
        serializer.save()
        return Response(data={
            'message': 'Registro actualizado.',
            'success': True
        }, status=HTTPStatus.OK)

    def delete(self, request, pk):
        try:
            obj = get_object_or_404(Materia, pk=pk)
        except Http404:
            return Response(data={
                'message': 'Objeto con la clave primaria proporcionada no encontrado.',
                'success': False
            }, status=HTTPStatus.NOT_FOUND)
        obj.delete()
        return Response(data={
            'message': 'Registro eliminado.',
            'success': True
        }, status=HTTPStatus.OK)
