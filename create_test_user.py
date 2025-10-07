#!/usr/bin/env python
"""
Script to create a test user for testing the login integration.
Run this after setting up the Django environment.
"""

import os
import sys
import django

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'queenbe_backend.settings')
django.setup()

from django.contrib.auth.models import User

def create_test_user():
    """Create a test user for login testing."""
    username = 'testuser'
    password = 'testpass123'
    email = 'test@queenbee.com'
    
    # Check if user already exists
    if User.objects.filter(username=username).exists():
        print(f"User '{username}' already exists!")
        user = User.objects.get(username=username)
    else:
        # Create the user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name='Test',
            last_name='User'
        )
        print(f"Test user created successfully!")
    
    print(f"Login credentials:")
    print(f"Username: {username}")
    print(f"Password: {password}")
    print(f"Email: {email}")
    
    return user

if __name__ == '__main__':
    create_test_user()
