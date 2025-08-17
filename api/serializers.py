from rest_framework import serializers
from .models import Student, Washerman, Order

class StudentSerializer(serializers.ModelSerializer):
    """Serializer for Student model"""
    
    class Meta:
        model = Student
        fields = ['bag_no', 'name', 'email', 'enrollment_no', 'phone_no', 'residency_no', 'created_at']
        read_only_fields = ['created_at']

class WashermanSerializer(serializers.ModelSerializer):
    """Serializer for Washerman model"""
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = Washerman
        fields = ['id', 'username', 'password', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        washerman = Washerman(**validated_data)
        washerman.password = password  # In production, this should be hashed
        washerman.save()
        return washerman

class OrderSerializer(serializers.ModelSerializer):
    """Serializer for Order model"""
    
    class Meta:
        model = Order
        fields = ['id', 'bag_no', 'number_of_clothes', 'submission_date', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'submission_date', 'created_at', 'updated_at']

class StudentSignupSerializer(serializers.Serializer):
    """Serializer for student signup"""
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    enrollment_no = serializers.CharField(max_length=20)
    bag_no = serializers.CharField(max_length=20)
    phone_no = serializers.CharField(max_length=15)
    residency_no = serializers.CharField(max_length=20)

    def validate(self, attrs):
        errors = {}
        if Student.objects.filter(email=attrs['email']).exists():
            errors['email'] = 'Email already exists'
        if Student.objects.filter(enrollment_no=attrs['enrollment_no']).exists():
            errors['enrollment_no'] = 'Enrollment number already exists'
        if Student.objects.filter(bag_no=attrs['bag_no']).exists():
            errors['bag_no'] = 'Bag number already exists'
        if errors:
            raise serializers.ValidationError(errors)
        return attrs

class WashermanSignupSerializer(serializers.Serializer):
    """Serializer for washerman signup"""
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)

class StudentLoginSerializer(serializers.Serializer):
    """Serializer for student login"""
    email = serializers.EmailField()
    enrollment_no = serializers.CharField(max_length=20)

class WashermanLoginSerializer(serializers.Serializer):
    """Serializer for washerman login"""
    username = serializers.CharField()
    password = serializers.CharField()

class CreateOrderSerializer(serializers.Serializer):
    """Serializer for creating orders"""
    bag_no = serializers.CharField(max_length=20)
    number_of_clothes = serializers.IntegerField(min_value=1, max_value=50)

class UpdateOrderStatusSerializer(serializers.Serializer):
    """Serializer for updating order status"""
    status = serializers.ChoiceField(choices=Order.STATUS_CHOICES)
