"""
Test script to demonstrate Customer API functionality
Run this after starting the Django development server
"""
import requests
import json
from datetime import date

# Base URL for the API
BASE_URL = "http://127.0.0.1:8000/api/customers/"

def test_customer_crud():
    """Test the complete CRUD operations for Customer API"""
    
    # Test data based on customer_model_definition.py
    customer_data = {
        "first_name": "John",
        "last_name": "Doe",
        "nickname": "Big J",
        "email": "john.doe@example.com",
        "phone": "5551234567",
        "date_of_birth": "1990-01-15",
        "gender": "male",
        "is_active": True,
        "address_street": "123 Main Street",
        "address_number": "Apt 4B",
        "address_neighborhood": "Downtown",
        "address_city": "New York",
        "address_state": "NY",
        "address_zip_code": "10001",
        "address_country": "USA",
        "preferences": ["whatsapp_news", "email_news"],
        "tags": ["VIP"]
    }
    
    print("=== Customer API Test ===\n")
    
    # 1. CREATE - POST /api/customers/
    print("1. Creating a new customer...")
    try:
        response = requests.post(BASE_URL, json=customer_data)
        print(f"Status: {response.status_code}")
        if response.status_code == 201:
            created_customer = response.json()
            customer_uuid = created_customer['uuid']
            print(f"✅ Customer created successfully with UUID: {customer_uuid}")
            print(f"Full name: {created_customer['full_name']}")
            print(f"Full address: {created_customer['full_address']}")
        else:
            print(f"❌ Error creating customer: {response.text}")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed. Make sure Django development server is running:")
        print("   python manage.py runserver")
        return
    
    print("\n" + "="*50 + "\n")
    
    # 2. READ - GET /api/customers/{uuid}/
    print(f"2. Retrieving customer {customer_uuid}...")
    response = requests.get(f"{BASE_URL}{customer_uuid}/")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        customer = response.json()
        print(f"✅ Customer retrieved: {customer['full_name']}")
    else:
        print(f"❌ Error retrieving customer: {response.text}")
    
    print("\n" + "="*50 + "\n")
    
    # 3. UPDATE - PATCH /api/customers/{uuid}/
    print(f"3. Updating customer {customer_uuid}...")
    update_data = {
        "nickname": "Johnny",
        "tags": ["VIP", "Diabetic"]
    }
    response = requests.patch(f"{BASE_URL}{customer_uuid}/", json=update_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        updated_customer = response.json()
        print(f"✅ Customer updated: {updated_customer['nickname']}")
        print(f"New tags: {updated_customer['tags']}")
    else:
        print(f"❌ Error updating customer: {response.text}")
    
    print("\n" + "="*50 + "\n")
    
    # 4. LIST - GET /api/customers/
    print("4. Listing all customers...")
    response = requests.get(BASE_URL)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        customers_data = response.json()
        print(f"✅ Found {customers_data['count']} customers")
        for customer in customers_data['results']:
            print(f"   - {customer['full_name']} ({customer['email']})")
    else:
        print(f"❌ Error listing customers: {response.text}")
    
    print("\n" + "="*50 + "\n")
    
    # 5. FILTER - GET /api/customers/?is_active=true
    print("5. Filtering active customers...")
    response = requests.get(f"{BASE_URL}?is_active=true")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        active_customers = response.json()
        print(f"✅ Found {active_customers['count']} active customers")
    else:
        print(f"❌ Error filtering customers: {response.text}")
    
    print("\n" + "="*50 + "\n")
    
    # 6. SEARCH - GET /api/customers/?search=John
    print("6. Searching for 'John'...")
    response = requests.get(f"{BASE_URL}?search=John")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        search_results = response.json()
        print(f"✅ Found {search_results['count']} customers matching 'John'")
    else:
        print(f"❌ Error searching customers: {response.text}")
    
    print("\n" + "="*50 + "\n")
    
    # 7. DEACTIVATE - POST /api/customers/{uuid}/deactivate/
    print(f"7. Deactivating customer {customer_uuid}...")
    response = requests.post(f"{BASE_URL}{customer_uuid}/deactivate/")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"✅ {result['message']}")
        print(f"Customer is_active: {result['customer']['is_active']}")
    else:
        print(f"❌ Error deactivating customer: {response.text}")
    
    print("\n" + "="*50 + "\n")
    
    # 8. ACTIVATE - POST /api/customers/{uuid}/activate/
    print(f"8. Activating customer {customer_uuid}...")
    response = requests.post(f"{BASE_URL}{customer_uuid}/activate/")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"✅ {result['message']}")
        print(f"Customer is_active: {result['customer']['is_active']}")
    else:
        print(f"❌ Error activating customer: {response.text}")
    
    print("\n" + "="*50 + "\n")
    
    # 9. DELETE - DELETE /api/customers/{uuid}/
    print(f"9. Deleting customer {customer_uuid}...")
    response = requests.delete(f"{BASE_URL}{customer_uuid}/")
    print(f"Status: {response.status_code}")
    if response.status_code == 204:
        print("✅ Customer deleted successfully")
    else:
        print(f"❌ Error deleting customer: {response.text}")
    
    print("\n" + "="*80)
    print("🎉 Customer API test completed!")
    print("="*80)


def print_api_endpoints():
    """Print all available API endpoints"""
    print("\n📋 Available API Endpoints:")
    print("="*50)
    
    endpoints = [
        ("GET", "/api/customers/", "List all customers (with pagination, filtering, search)"),
        ("POST", "/api/customers/", "Create a new customer"),
        ("GET", "/api/customers/{uuid}/", "Retrieve a specific customer"),
        ("PUT", "/api/customers/{uuid}/", "Update a specific customer (full update)"),
        ("PATCH", "/api/customers/{uuid}/", "Partial update a specific customer"),
        ("DELETE", "/api/customers/{uuid}/", "Delete a specific customer"),
        ("GET", "/api/customers/active/", "List only active customers"),
        ("POST", "/api/customers/{uuid}/deactivate/", "Deactivate a customer"),
        ("POST", "/api/customers/{uuid}/activate/", "Activate a customer"),
        ("GET", "/api/customers/search_advanced/", "Advanced search with multiple criteria"),
    ]
    
    for method, endpoint, description in endpoints:
        print(f"{method:6} {endpoint:35} - {description}")
    
    print("\n🔍 Query Parameters:")
    print("="*50)
    filters = [
        ("?is_active=true/false", "Filter by active status"),
        ("?gender=male/female/other", "Filter by gender"),
        ("?address_country=USA", "Filter by country"),
        ("?address_state=NY", "Filter by state"),
        ("?address_city=New York", "Filter by city"),
        ("?search=John", "Search in first_name, last_name, nickname, email, phone"),
        ("?ordering=created_at,-updated_at", "Sort results (- for descending)"),
        ("?name=John", "Advanced search in names"),
        ("?location=New York", "Advanced search in location fields"),
        ("?tags=VIP,Diabetic", "Advanced search by tags (comma-separated)"),
        ("?preferences=whatsapp_news", "Advanced search by preferences"),
    ]
    
    for param, description in filters:
        print(f"{param:35} - {description}")


if __name__ == "__main__":
    print_api_endpoints()
    print("\n" + "="*80)
    print("🚀 Starting Customer API Tests...")
    print("Make sure to run 'python manage.py runserver' first!")
    print("="*80)
    
    # Uncomment the line below to run the tests
    # test_customer_crud()
    
    print("\nTo run the tests, uncomment the test_customer_crud() call at the bottom of this file")
    print("or run: python -c \"from customer_relationship.test_customer_api import test_customer_crud; test_customer_crud()\"")