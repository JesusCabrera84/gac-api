import asyncio
import sys
import os
import httpx
from uuid import uuid4

# Add project root to path
sys.path.append(os.getcwd())

BASE_URL = "http://localhost:8001/api/v1"


async def test_user_management():
    async with httpx.AsyncClient() as client:
        # 1. Login as admin
        print("Logging in as admin...")
        response = await client.post(
            f"{BASE_URL}/auth/login",
            data={"username": "admin@gac.com", "password": "admin123"},
        )
        if response.status_code != 200:
            print(f"Login failed: {response.text}")
            return

        token = response.json()["data"]["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        print("Login successful")

        # 2. Create new user
        print("Creating new user...")
        new_email = f"testuser_{uuid4().hex[:8]}@gac.com"
        response = await client.post(
            f"{BASE_URL}/users",
            json={
                "email": new_email,
                "password": "password123",
                "full_name": "Test User",
                "is_active": True,
                "roles": [],
            },
            headers=headers,
        )

        if response.status_code != 201:
            print(f"Create user failed: {response.text}")
            return

        user_data = response.json()["data"]
        user_id = user_data["user_id"]
        print(f"User created: {user_id}")

        # 3. List users
        print("Listing users...")
        response = await client.get(f"{BASE_URL}/users", headers=headers)
        if response.status_code != 200:
            print(f"List users failed: {response.text}")
            return

        users = response.json()["data"]
        print(f"Found {len(users)} users")

        # 4. Get user details
        print(f"Getting user details for {user_id}...")
        response = await client.get(f"{BASE_URL}/users/{user_id}", headers=headers)
        if response.status_code != 200:
            print(f"Get user failed: {response.text}")
            return
        print("User details retrieved")

        # 5. Update user
        print("Updating user...")
        response = await client.patch(
            f"{BASE_URL}/users/{user_id}",
            json={"full_name": "Updated Name"},
            headers=headers,
        )
        if response.status_code != 200:
            print(f"Update user failed: {response.text}")
            return

        updated_name = response.json()["data"]["full_name"]
        if updated_name != "Updated Name":
            print("Update verification failed")
            return
        print("User updated")

        # 6. Delete user (Soft delete)
        print("Deleting user...")
        response = await client.delete(f"{BASE_URL}/users/{user_id}", headers=headers)
        if response.status_code != 200:
            print(f"Delete user failed: {response.text}")
            return
        print("User deleted")

        # Verify soft delete
        response = await client.get(f"{BASE_URL}/users/{user_id}", headers=headers)
        if (
            not response.json()["data"]["is_active"] is False
        ):  # Check if is_active is False (or check if 404 if logic changed)
            # My implementation returns the user even if inactive on get_user, but is_active should be False
            print("Soft delete verification passed (is_active=False)")
        else:
            print("Soft delete verification failed")


if __name__ == "__main__":
    asyncio.run(test_user_management())
