#!/usr/bin/env python
import sys
import os
import django
from django.core.management import execute_from_command_line
import importlib

def check_dependencies():
    """Check if all required packages are installed"""
    required_packages = [
        'django',
        'channels',
        'pyserial',
        'python-dotenv'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"✓ {package} is installed")
        except ImportError:
            missing_packages.append(package)
            print(f"✗ {package} is missing")
    
    return len(missing_packages) == 0

def check_django_setup():
    """Check if Django project is properly configured"""
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web_interface.settings')
        django.setup()
        from django.conf import settings
        print("✓ Django settings are properly configured")
        return True
    except Exception as e:
        print(f"✗ Django setup failed: {str(e)}")
        return False

def check_static_files():
    """Check if static files are properly configured"""
    from django.conf import settings
    
    if not os.path.exists(settings.STATIC_ROOT):
        print("✗ Static root directory does not exist")
        return False
    
    if not os.path.exists(os.path.join(settings.BASE_DIR, 'static')):
        print("✗ Static directory does not exist")
        return False
    
    print("✓ Static files are properly configured")
    return True

def check_database():
    """Check if database is properly configured and migrated"""
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM sqlite_master")
        print("✓ Database is properly configured")
        return True
    except Exception as e:
        print(f"✗ Database check failed: {str(e)}")
        return False

def main():
    """Run all checks"""
    print("\nChecking Arduino Sensor Dashboard Setup...")
    print("-" * 40)
    
    all_passed = True
    
    print("\n1. Checking Dependencies:")
    if not check_dependencies():
        all_passed = False
    
    print("\n2. Checking Django Setup:")
    if not check_django_setup():
        all_passed = False
    
    print("\n3. Checking Static Files:")
    if not check_static_files():
        all_passed = False
    
    print("\n4. Checking Database:")
    if not check_database():
        all_passed = False
    
    print("\n" + "-" * 40)
    if all_passed:
        print("✓ All checks passed! The system is properly configured.")
        print("\nYou can now run the server with:")
        print("python manage.py runserver")
    else:
        print("✗ Some checks failed. Please fix the issues above and try again.")
    
    return 0 if all_passed else 1

if __name__ == '__main__':
    sys.exit(main()) 