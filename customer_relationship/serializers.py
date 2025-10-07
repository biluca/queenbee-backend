from rest_framework import serializers
from .models import Customer, AppointmentType, Appointment


class CustomerSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    full_address = serializers.ReadOnlyField()
    
    class Meta:
        model = Customer
        fields = [
            'uuid', 'first_name', 'last_name', 'nickname', 'email', 'phone',
            'date_of_birth', 'gender', 'created_at', 'updated_at', 'is_active',
            'address_street', 'address_number', 'address_neighborhood',
            'address_city', 'address_state', 'address_zip_code', 'address_country',
            'preferences', 'tags', 'full_name', 'full_address'
        ]
        read_only_fields = ['uuid', 'created_at', 'updated_at']
    
    def validate_preferences(self, value):
        """Validate preferences against allowed choices"""
        if not isinstance(value, list):
            raise serializers.ValidationError("Preferences must be a list.")
        
        valid_preferences = [choice[0] for choice in Customer.PREFERENCES_CHOICES]
        for pref in value:
            if pref not in valid_preferences:
                raise serializers.ValidationError(
                    f"'{pref}' is not a valid preference. "
                    f"Valid choices are: {', '.join(valid_preferences)}"
                )
        return value
    
    def validate_tags(self, value):
        """Validate tags against allowed choices"""
        if not isinstance(value, list):
            raise serializers.ValidationError("Tags must be a list.")
        
        valid_tags = [choice[0] for choice in Customer.TAGS_CHOICES]
        for tag in value:
            if tag not in valid_tags:
                raise serializers.ValidationError(
                    f"'{tag}' is not a valid tag. "
                    f"Valid choices are: {', '.join(valid_tags)}"
                )
        return value


class CustomerCreateSerializer(CustomerSerializer):
    """Serializer for creating customers with required fields validation"""
    
    class Meta(CustomerSerializer.Meta):
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email': {'required': True},
            'phone': {'required': True},
            'date_of_birth': {'required': True},
            'gender': {'required': True},
            'address_street': {'required': True},
            'address_number': {'required': True},
            'address_neighborhood': {'required': True},
            'address_city': {'required': True},
            'address_state': {'required': True},
            'address_zip_code': {'required': True},
            'address_country': {'required': True},
        }


class CustomerUpdateSerializer(CustomerSerializer):
    """Serializer for updating customers with optional fields"""
    
    class Meta(CustomerSerializer.Meta):
        pass


class AppointmentTypeSerializer(serializers.ModelSerializer):
    """Serializer for AppointmentType model"""
    
    class Meta:
        model = AppointmentType
        fields = ['uuid', 'description', 'created_at', 'updated_at']
        read_only_fields = ['uuid', 'created_at', 'updated_at']


class AppointmentTypeCreateSerializer(AppointmentTypeSerializer):
    """Serializer for creating appointment types with required fields validation"""
    
    class Meta(AppointmentTypeSerializer.Meta):
        extra_kwargs = {
            'description': {'required': True},
        }


class AppointmentTypeUpdateSerializer(AppointmentTypeSerializer):
    """Serializer for updating appointment types with optional fields"""
    
    class Meta(AppointmentTypeSerializer.Meta):
        pass


class AppointmentSerializer(serializers.ModelSerializer):
    """Serializer for Appointment model"""
    customer_name = serializers.CharField(source='customer.full_name', read_only=True)
    appointment_type_description = serializers.CharField(source='appointment_type.description', read_only=True)
    duration_minutes = serializers.ReadOnlyField()
    
    class Meta:
        model = Appointment
        fields = [
            'uuid', 'customer', 'customer_name', 'appointment_type', 'appointment_type_description',
            'start_time', 'end_time', 'status', 'notes', 'cancellation_reason',
            'created_at', 'updated_at', 'duration_minutes'
        ]
        read_only_fields = ['uuid', 'created_at', 'updated_at']
    
    def validate(self, data):
        """Validate that end_time is after start_time"""
        if 'start_time' in data and 'end_time' in data:
            if data['end_time'] <= data['start_time']:
                raise serializers.ValidationError("End time must be after start time.")
        return data
    
    def validate_status(self, value):
        """Validate status against allowed choices"""
        valid_statuses = [choice[0] for choice in Appointment.STATUS_CHOICES]
        if value not in valid_statuses:
            raise serializers.ValidationError(
                f"'{value}' is not a valid status. "
                f"Valid choices are: {', '.join(valid_statuses)}"
            )
        return value


class AppointmentCreateSerializer(AppointmentSerializer):
    """Serializer for creating appointments with required fields validation"""
    
    class Meta(AppointmentSerializer.Meta):
        extra_kwargs = {
            'customer': {'required': True},
            'appointment_type': {'required': True},
            'start_time': {'required': True},
            'end_time': {'required': True},
        }


class AppointmentUpdateSerializer(AppointmentSerializer):
    """Serializer for updating appointments with optional fields"""
    
    class Meta(AppointmentSerializer.Meta):
        pass