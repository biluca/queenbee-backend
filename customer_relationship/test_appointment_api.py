#!/usr/bin/env python3
"""
Test script for Appointment and AppointmentType API endpoints
Run this script to test the CRUD operations for appointments
"""

import json
import requests
from datetime import datetime, timedelta
from django.utils import timezone

# Base API URL
BASE_URL = "http://127.0.0.1:8000/api"

def test_api_endpoint(method, url, data=None, expected_status=200):
    """Helper function to test API endpoints"""
    try:
        response = requests.request(method, url, json=data)
        print(f"{method} {url}")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == expected_status:
            print("✅ Success")
            if response.content:
                return response.json()
        else:
            print(f"❌ Expected {expected_status}, got {response.status_code}")
            print(f"Response: {response.text}")
        
        print("-" * 50)
        return None
        
    except requests.exceptions.ConnectionError:
        print(f"❌ Connection Error: Make sure Django server is running on {BASE_URL}")
        print("Run: python manage.py runserver")
        return None
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None


def main():
    print("🚀 Testing Appointment API Endpoints")
    print("=" * 50)
    
    # Test AppointmentType endpoints
    print("\n📝 Testing AppointmentType Endpoints")
    print("-" * 50)
    
    # 1. List all appointment types
    appointment_types = test_api_endpoint("GET", f"{BASE_URL}/appointment-types/")
    
    if appointment_types and appointment_types.get('results'):
        appointment_type_uuid = appointment_types['results'][0]['uuid']
        
        # 2. Get specific appointment type
        test_api_endpoint("GET", f"{BASE_URL}/appointment-types/{appointment_type_uuid}/")
        
        # 3. Create new appointment type
        new_type_data = {
            "description": "API Test Appointment Type"
        }
        created_type = test_api_endpoint("POST", f"{BASE_URL}/appointment-types/", new_type_data, 201)
        
        if created_type:
            created_type_uuid = created_type['uuid']
            
            # 4. Update appointment type
            update_data = {
                "description": "Updated API Test Appointment Type"
            }
            test_api_endpoint("PATCH", f"{BASE_URL}/appointment-types/{created_type_uuid}/", update_data)
            
            # 5. Delete appointment type
            test_api_endpoint("DELETE", f"{BASE_URL}/appointment-types/{created_type_uuid}/", expected_status=204)
    
    # Test Appointment endpoints
    print("\n📅 Testing Appointment Endpoints")
    print("-" * 50)
    
    # 1. List all appointments
    appointments = test_api_endpoint("GET", f"{BASE_URL}/appointments/")
    
    # 2. Get today's appointments
    test_api_endpoint("GET", f"{BASE_URL}/appointments/today/")
    
    # 3. Get upcoming appointments
    test_api_endpoint("GET", f"{BASE_URL}/appointments/upcoming/")
    
    if appointments and appointments.get('results'):
        appointment_uuid = appointments['results'][0]['uuid']
        customer_uuid = appointments['results'][0]['customer']
        
        # 4. Get specific appointment
        test_api_endpoint("GET", f"{BASE_URL}/appointments/{appointment_uuid}/")
        
        # 5. Get appointments by customer
        test_api_endpoint("GET", f"{BASE_URL}/appointments/by_customer/?customer_uuid={customer_uuid}")
        
        # 6. Confirm appointment
        test_api_endpoint("POST", f"{BASE_URL}/appointments/{appointment_uuid}/confirm/")
        
        # 7. Cancel appointment with reason
        cancel_data = {
            "cancellation_reason": "Customer requested cancellation for testing"
        }
        test_api_endpoint("POST", f"{BASE_URL}/appointments/{appointment_uuid}/cancel/", cancel_data)
    
    # Test creating a new appointment (if we have customers and appointment types)
    customers = test_api_endpoint("GET", f"{BASE_URL}/customers/")
    appointment_types = test_api_endpoint("GET", f"{BASE_URL}/appointment-types/")
    
    if (customers and customers.get('results') and 
        appointment_types and appointment_types.get('results')):
        
        customer_uuid = customers['results'][0]['uuid']
        appointment_type_uuid = appointment_types['results'][0]['uuid']
        
        # Create new appointment
        now = datetime.now()
        start_time = now + timedelta(days=1)  # Tomorrow
        end_time = start_time + timedelta(hours=1)  # 1 hour appointment
        
        new_appointment_data = {
            "customer": customer_uuid,
            "appointment_type": appointment_type_uuid,
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "status": "scheduled",
            "notes": "API test appointment"
        }
        
        created_appointment = test_api_endpoint("POST", f"{BASE_URL}/appointments/", new_appointment_data, 201)
        
        if created_appointment:
            created_appointment_uuid = created_appointment['uuid']
            
            # Update the appointment
            update_data = {
                "notes": "Updated API test appointment",
                "status": "confirmed"
            }
            test_api_endpoint("PATCH", f"{BASE_URL}/appointments/{created_appointment_uuid}/", update_data)
            
            # Delete the test appointment
            test_api_endpoint("DELETE", f"{BASE_URL}/appointments/{created_appointment_uuid}/", expected_status=204)
    
    print("\n🎉 API Testing Complete!")
    print("Check the output above for any failed tests (❌)")
    print("All successful tests are marked with ✅")


if __name__ == "__main__":
    main()