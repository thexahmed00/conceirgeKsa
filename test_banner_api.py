#!/usr/bin/env python
"""
Test script demonstrating the Admin Banner API endpoints.

This shows how to use the new banner CRUD operations.
"""

import requests
import json

# API base URL - adjust to your environment
BASE_URL = "http://localhost:8000/api/v1/content"

# Sample admin JWT token (you'll need to get this from login)
ADMIN_TOKEN = "your_admin_jwt_token_here"

headers = {
    "Authorization": f"Bearer {ADMIN_TOKEN}",
    "Content-Type": "application/json",
}


def test_create_banner():
    """Test creating a new banner."""
    print("\n=== CREATE BANNER ===")
    
    banner_payload = {
        "title": "Summer Sale 50% Off",
        "image_url": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=1000",
        "description": "Check out our summer collection with amazing discounts",
        "link_url": "app://promo/summer-2025",
        "display_order": 1,
        "is_active": True
    }
    
    print(f"Creating banner with payload: {json.dumps(banner_payload, indent=2)}")
    response = requests.post(
        f"{BASE_URL}/admin/banners",
        json=banner_payload,
        headers=headers
    )
    
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Response: {json.dumps(result, indent=2)}")
    
    return result.get("id") if response.status_code == 201 else None


def test_list_banners():
    """Test listing banners (public endpoint)."""
    print("\n=== LIST BANNERS (Public) ===")
    
    response = requests.get(f"{BASE_URL}/banners")
    
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Found {result.get('total', 0)} banners")
    print(f"Response: {json.dumps(result, indent=2)}")


def test_update_banner(banner_id):
    """Test updating a banner."""
    print(f"\n=== UPDATE BANNER {banner_id} ===")
    
    update_payload = {
        "title": "Summer Sale 70% Off - UPDATED",
        "display_order": 2,
        "is_active": True
    }
    
    print(f"Updating banner with payload: {json.dumps(update_payload, indent=2)}")
    response = requests.put(
        f"{BASE_URL}/admin/banners/{banner_id}",
        json=update_payload,
        headers=headers
    )
    
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Response: {json.dumps(result, indent=2)}")


def test_delete_banner(banner_id):
    """Test deleting a banner."""
    print(f"\n=== DELETE BANNER {banner_id} ===")
    
    response = requests.delete(
        f"{BASE_URL}/admin/banners/{banner_id}",
        headers=headers
    )
    
    print(f"Status: {response.status_code}")
    if response.content:
        print(f"Response: {response.json()}")
    else:
        print("Banner deleted successfully (no content returned)")


if __name__ == "__main__":
    print("Admin Banner API Test Script")
    print("=" * 50)
    
    # List banners (public)
    test_list_banners()
    
    # Create a banner
    banner_id = test_create_banner()
    
    if banner_id:
        # List banners again
        test_list_banners()
        
        # Update the banner
        test_update_banner(banner_id)
        
        # Delete the banner
        test_delete_banner(banner_id)
        
        # List banners again
        test_list_banners()
    else:
        print("\nFailed to create banner - skipping update and delete tests")
    
    print("\n" + "=" * 50)
    print("Test script complete!")
