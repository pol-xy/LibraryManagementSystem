# create_admin.py - Create default admin user
from backend.auth import AuthSystem

def create_admin_user():
    """Create default admin user"""
    auth = AuthSystem()
    
    print("=" * 60)
    print("CREATING DEFAULT ADMIN USER")
    print("=" * 60)
    
    # Admin credentials
    username = "admin"
    email = "admin@library.com"
    password = "Admin@123"  # Strong password
    role = "admin"
    
    print(f"Username: {username}")
    print(f"Email: {email}")
    print(f"Role: {role}")
    print("-" * 60)
    
    # Check if admin already exists
    try:
        success, message = auth.register_user(username, email, password, role)
        
        if success:
            print(f"✅ {message}")
            print("\nAdmin credentials:")
            print(f"  Username: {username}")
            print(f"  Password: {password}")
            print(f"  Email: {email}")
            print("\n⚠️ IMPORTANT: Change this password after first login!")
        else:
            print(f"❌ {message}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("=" * 60)

if __name__ == "__main__":
    create_admin_user()