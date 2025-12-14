# backend/auth.py
import hashlib
import secrets
import string
from datetime import datetime
from database.db_connection import get_db_connection

class AuthSystem:
    def __init__(self):
        self.db = get_db_connection()
        self.current_user = None
    
    def hash_password(self, password, salt=None):
        """Hash password with salt using SHA-256"""
        if salt is None:
            salt = secrets.token_hex(16)
        
        # Combine password and salt
        password_salt = password + salt
        # Hash using SHA-256
        hash_object = hashlib.sha256(password_salt.encode())
        password_hash = hash_object.hexdigest()
        
        return password_hash, salt
    
    def verify_password(self, password, stored_hash, salt):
        """Verify password against stored hash"""
        password_hash, _ = self.hash_password(password, salt)
        return password_hash == stored_hash
    
    def generate_secure_password(self, length=12):
        """Generate a secure random password"""
        characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(secrets.choice(characters) for _ in range(length))
    
    def validate_email(self, email):
        """Validate email format"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def validate_password_strength(self, password):
        """Validate password strength"""
        if len(password) < 8:
            return False, "Password must be at least 8 characters"
        
        if not any(c.isupper() for c in password):
            return False, "Password must contain at least one uppercase letter"
        
        if not any(c.islower() for c in password):
            return False, "Password must contain at least one lowercase letter"
        
        if not any(c.isdigit() for c in password):
            return False, "Password must contain at least one digit"
        
        return True, "Password is strong"
    
    # ========== USER REGISTRATION ==========
    
    def register_user(self, username, email, password, role='borrower'):
        """Register a new user"""
        # Validate inputs
        if not username or not email or not password:
            return False, "All fields are required"
        
        if not self.validate_email(email):
            return False, "Invalid email format"
        
        # Check if username or email already exists
        check_query = """
        SELECT user_id FROM users WHERE username = %s OR email = %s
        """
        existing = self.db.execute_query(check_query, (username, email), fetch=True)
        
        if existing:
            return False, "Username or email already exists"
        
        # Validate password strength
        is_valid, message = self.validate_password_strength(password)
        if not is_valid:
            return False, message
        
        # Hash password
        password_hash, salt = self.hash_password(password)
        
        # Insert user
        insert_query = """
        INSERT INTO users (username, email, password_hash, salt, role)
        VALUES (%s, %s, %s, %s, %s)
        """
        
        try:
            user_id = self.db.execute_query(
                insert_query, 
                (username, email, password_hash, salt, role)
            )
            
            if user_id:
                # Create linked borrower record
                borrower_query = """
                INSERT INTO borrowers (name, email, user_id)
                VALUES (%s, %s, %s)
                """
                self.db.execute_query(
                    borrower_query,
                    (username, email, user_id)
                )
                
                return True, f"User '{username}' registered successfully! User ID: {user_id}"
            else:
                return False, "Registration failed"
                
        except Exception as e:
            return False, f"Registration error: {str(e)}"
    
    # ========== USER LOGIN ==========
    
    def login(self, username_or_email, password):
        """Authenticate user"""
        if not username_or_email or not password:
            return False, "Username/email and password are required"
        
        # Find user by username or email
        query = """
        SELECT user_id, username, email, password_hash, salt, role, is_active
        FROM users 
        WHERE (username = %s OR email = %s) AND is_active = TRUE
        """
        
        result = self.db.execute_query(query, (username_or_email, username_or_email), fetch=True)
        
        if not result:
            return False, "Invalid username/email or password"
        
        user = result[0]
        
        # Verify password
        if not self.verify_password(password, user['password_hash'], user['salt']):
            return False, "Invalid username/email or password"
        
        # Update last login
        update_query = """
        UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE user_id = %s
        """
        self.db.execute_query(update_query, (user['user_id'],))
        
        # Store current user
        self.current_user = {
            'user_id': user['user_id'],
            'username': user['username'],
            'email': user['email'],
            'role': user['role'],
            'is_active': user['is_active']
        }
        
        return True, f"Login successful! Welcome {user['username']}"
    
    # ========== USER MANAGEMENT ==========
    
    def get_current_user(self):
        """Get current logged in user"""
        return self.current_user
    
    def logout(self):
        """Logout current user"""
        self.current_user = None
        return True, "Logged out successfully"
    
    def change_password(self, user_id, old_password, new_password):
        """Change user password"""
        # Get current password hash
        query = "SELECT password_hash, salt FROM users WHERE user_id = %s"
        result = self.db.execute_query(query, (user_id,), fetch=True)
        
        if not result:
            return False, "User not found"
        
        stored_hash = result[0]['password_hash']
        salt = result[0]['salt']
        
        # Verify old password
        if not self.verify_password(old_password, stored_hash, salt):
            return False, "Current password is incorrect"
        
        # Validate new password strength
        is_valid, message = self.validate_password_strength(new_password)
        if not is_valid:
            return False, message
        
        # Hash new password
        new_hash, new_salt = self.hash_password(new_password)
        
        # Update password
        update_query = """
        UPDATE users 
        SET password_hash = %s, salt = %s 
        WHERE user_id = %s
        """
        
        success = self.db.execute_query(
            update_query, 
            (new_hash, new_salt, user_id)
        )
        
        if success:
            return True, "Password changed successfully"
        else:
            return False, "Failed to change password"
    
    def reset_password_request(self, email):
        """Initiate password reset (simplified version)"""
        # Check if email exists
        query = "SELECT user_id FROM users WHERE email = %s"
        result = self.db.execute_query(query, (email,), fetch=True)
        
        if not result:
            return False, "Email not found in our system"
        
        # In a real system, you would:
        # 1. Generate a reset token
        # 2. Send email with reset link
        # 3. Store token in database with expiration
        
        # For now, just return success
        return True, "Password reset instructions sent to your email"
    
    def update_profile(self, user_id, username=None, email=None):
        """Update user profile"""
        updates = []
        params = []
        
        if username:
            # Check if username already taken by another user
            check_query = """
            SELECT user_id FROM users 
            WHERE username = %s AND user_id != %s
            """
            existing = self.db.execute_query(check_query, (username, user_id), fetch=True)
            if existing:
                return False, "Username already taken"
            updates.append("username = %s")
            params.append(username)
        
        if email:
            if not self.validate_email(email):
                return False, "Invalid email format"
            
            # Check if email already taken by another user
            check_query = """
            SELECT user_id FROM users 
            WHERE email = %s AND user_id != %s
            """
            existing = self.db.execute_query(check_query, (email, user_id), fetch=True)
            if existing:
                return False, "Email already registered"
            
            updates.append("email = %s")
            params.append(email)
        
        if not updates:
            return False, "No updates provided"
        
        # Build query
        params.append(user_id)
        query = f"""
        UPDATE users 
        SET {', '.join(updates)} 
        WHERE user_id = %s
        """
        
        success = self.db.execute_query(query, params)
        
        if success:
            # Also update borrower record if linked
            if email or username:
                borrower_updates = []
                borrower_params = []
                
                if username:
                    borrower_updates.append("name = %s")
                    borrower_params.append(username)
                if email:
                    borrower_updates.append("email = %s")
                    borrower_params.append(email)
                
                if borrower_updates:
                    borrower_params.append(user_id)
                    borrower_query = f"""
                    UPDATE borrowers 
                    SET {', '.join(borrower_updates)} 
                    WHERE user_id = %s
                    """
                    self.db.execute_query(borrower_query, borrower_params)
            
            return True, "Profile updated successfully"
        else:
            return False, "Failed to update profile"