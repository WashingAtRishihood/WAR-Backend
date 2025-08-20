from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.db import transaction
from .models import Student, Washerman, Order
from .serializers import (
    StudentSerializer, UpdateOrderCountSerializer, WashermanSerializer, OrderSerializer,
    StudentSignupSerializer, WashermanSignupSerializer,
    StudentLoginSerializer, WashermanLoginSerializer,
    CreateOrderSerializer, UpdateOrderStatusSerializer
)

# Authentication Views
class StudentLoginView(APIView):
    """Student login endpoint"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = StudentLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            
            try:
                student = Student.objects.get(email=email, password=password)  # In production, use proper password hashing
                return Response({
                    'message': 'Login successful',
                    'student': StudentSerializer(student).data
                }, status=status.HTTP_200_OK)
            except Student.DoesNotExist:
                return Response({'error': 'Invalid email or password'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WashermanLoginView(APIView):
    """Washerman login endpoint"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = WashermanLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            
            try:
                washerman = Washerman.objects.get(username=username, password=password)
                return Response({
                    'message': 'Login successful',
                    'washerman': WashermanSerializer(washerman).data
                }, status=status.HTTP_200_OK)
            except Washerman.DoesNotExist:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StudentSignupView(APIView):
    """Student registration endpoint"""
    permission_classes = [AllowAny]
    
    @transaction.atomic
    def post(self, request):
        email = request.data.get('email', '')
        if not email.endswith('rishihood.edu.in'):
            return Response(
                {'error': 'Please use your Rishihood University email'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        serializer = StudentSignupSerializer(data=request.data)
        if serializer.is_valid():
            student = Student.objects.create(**serializer.validated_data)
            
            return Response({
                'message': 'Student registered successfully',
                'student': StudentSerializer(student).data
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WashermanSignupView(APIView):
    """Washerman registration endpoint"""
    permission_classes = [AllowAny]
    
    @transaction.atomic
    def post(self, request):
        serializer = WashermanSignupSerializer(data=request.data)
        if serializer.is_valid():
            washerman = Washerman.objects.create(**serializer.validated_data)
            
            return Response({
                'message': 'Washerman registered successfully',
                'washerman': WashermanSerializer(washerman).data
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Order Views
class CreateOrderView(APIView):
    """Create new order endpoint"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = CreateOrderSerializer(data=request.data)
        if serializer.is_valid():
            bag_no = serializer.validated_data['bag_no']
            
            # Verify student exists
            try:
                student = Student.objects.get(bag_no=bag_no)
                order = Order.objects.create(**serializer.validated_data)
                
                return Response({
                    'message': 'Order created successfully',
                    'order': OrderSerializer(order).data
                }, status=status.HTTP_201_CREATED)
            except Student.DoesNotExist:
                return Response({'error': 'Student with this bag number not found'}, 
                              status=status.HTTP_404_NOT_FOUND)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StudentOrdersView(APIView):
    """Get orders for a specific student"""
    permission_classes = [AllowAny]
    
    def get(self, request, bag_no):
        try:
            student = Student.objects.get(bag_no=bag_no)
            orders = Order.objects.filter(bag_no=bag_no)
            serializer = OrderSerializer(orders, many=True)
            
            return Response({
                'student': StudentSerializer(student).data,
                'orders': serializer.data
            })
        except Student.DoesNotExist:
            return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)

class AllOrdersView(APIView):
    """Get all orders (for washerman dashboard)"""
    permission_classes = [AllowAny]
    
    def get(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

class PendingOrdersView(APIView):
    """Get pending orders for washerman"""
    permission_classes = [AllowAny]
    
    def get(self, request):
        pending_orders = Order.objects.filter(status='pending')
        serializer = OrderSerializer(pending_orders, many=True)
        return Response(serializer.data)

class UpdateOrderStatusView(APIView):
    """Update order status (Received/Ready buttons)"""
    permission_classes = [AllowAny]
    
    def put(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
            serializer = UpdateOrderStatusSerializer(data=request.data)
            
            if serializer.is_valid():
                new_status = serializer.validated_data['status']
                
                # Validate status transitions
                if order.status == 'pending' and new_status == 'inprogress':
                    # Washerman clicked "Received"
                    order.status = new_status
                    order.save()
                elif order.status == 'inprogress' and new_status == 'complete':
                    # Washerman clicked "Ready"
                    order.status = new_status
                    order.save()
                else:
                    return Response({'error': 'Invalid status transition'}, 
                                  status=status.HTTP_400_BAD_REQUEST)
                
                return Response({
                    'message': 'Order status updated successfully',
                    'order': OrderSerializer(order).data
                })
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)


class UpdateOrderCountView(APIView):
    """Update number_of_clothes for an order"""
    permission_classes = [AllowAny]

    def put(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
            serializer = UpdateOrderCountSerializer(data=request.data)
            if serializer.is_valid():
                order.number_of_clothes = serializer.validated_data['number_of_clothes']
                order.save()
                return Response({
                    'message': 'Order count updated successfully',
                    'order': OrderSerializer(order).data
                })
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

# Dashboard Views
class StudentDashboardView(APIView):
    """Get student dashboard data"""
    permission_classes = [AllowAny]
    
    def get(self, request, bag_no):
        try:
            student = Student.objects.get(bag_no=bag_no)
            orders = Order.objects.filter(bag_no=bag_no)
            
            dashboard_data = {
                'student': StudentSerializer(student).data,
                'total_orders': orders.count(),
                'pending_orders': orders.filter(status='pending').count(),
                'inprogress_orders': orders.filter(status='inprogress').count(),
                'complete_orders': orders.filter(status='complete').count(),
                'recent_orders': OrderSerializer(orders[:5], many=True).data
            }
            
            return Response(dashboard_data)
        except Student.DoesNotExist:
            return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)

class WashermanDashboardView(APIView):
    """Get washerman dashboard data"""
    permission_classes = [AllowAny]
    
    def get(self, request):
        orders = Order.objects.all()
        
        dashboard_data = {
            'total_orders': orders.count(),
            'pending_orders': orders.filter(status='pending').count(),
            'inprogress_orders': orders.filter(status='inprogress').count(),
            'complete_orders': orders.filter(status='complete').count(),
            'recent_orders': OrderSerializer(orders[:10], many=True).data
        }
        
        return Response(dashboard_data)
