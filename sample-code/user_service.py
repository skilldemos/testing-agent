"""
Sample E-Commerce Module - User Service

This module handles user account management for an e-commerce platform.
It demonstrates various testing scenarios including:
- Input validation
- Database interactions
- External API calls
- Error handling
- Business logic
"""

import re
import hashlib
from typing import Optional, Dict, List
from datetime import datetime, timedelta


class UserValidationError(Exception):
    """Raised when user data fails validation."""
    pass


class DatabaseError(Exception):
    """Raised when database operations fail."""
    pass


class EmailService:
    """External email service for sending notifications."""
    
    def send_welcome_email(self, email: str, name: str) -> bool:
        """
        Send a welcome email to a new user.
        
        Args:
            email: User's email address
            name: User's display name
            
        Returns:
            True if email sent successfully
            
        Raises:
            ConnectionError: If email service is unavailable
        """
        # In real implementation, this would call an external API
        if not email or '@' not in email:
            return False
        return True


class Database:
    """Database abstraction for user storage."""
    
    def __init__(self):
        self.users = {}
    
    def save_user(self, user_data: Dict) -> int:
        """
        Save user to database.
        
        Args:
            user_data: Dictionary containing user information
            
        Returns:
            User ID assigned by database
            
        Raises:
            DatabaseError: If save operation fails
        """
        # Simulate database behavior
        if 'email' not in user_data:
            raise DatabaseError("Email is required")
        
        user_id = len(self.users) + 1
        self.users[user_id] = user_data
        return user_id
    
    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """
        Retrieve user by email address.
        
        Args:
            email: Email to search for
            
        Returns:
            User dictionary if found, None otherwise
        """
        for user in self.users.values():
            if user.get('email') == email:
                return user
        return None
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        """Retrieve user by ID."""
        return self.users.get(user_id)
    
    def update_user(self, user_id: int, updates: Dict) -> bool:
        """Update user information."""
        if user_id not in self.users:
            return False
        self.users[user_id].update(updates)
        return True


class UserService:
    """
    Service for managing user accounts.
    
    This service handles user registration, authentication,
    and profile management.
    """
    
    MIN_PASSWORD_LENGTH = 8
    MAX_NAME_LENGTH = 100
    
    def __init__(self, database: Database, email_service: EmailService):
        """
        Initialize UserService.
        
        Args:
            database: Database instance for storing users
            email_service: Service for sending emails
        """
        self.db = database
        self.email_service = email_service
    
    def validate_email(self, email: str) -> bool:
        """
        Validate email address format.
        
        Args:
            email: Email address to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not email or not isinstance(email, str):
            return False
        
        # Simple regex for email validation
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    def validate_password(self, password: str) -> bool:
        """
        Validate password meets security requirements.
        
        Password must:
        - Be at least 8 characters long
        - Contain at least one uppercase letter
        - Contain at least one lowercase letter
        - Contain at least one number
        
        Args:
            password: Password to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not password or len(password) < self.MIN_PASSWORD_LENGTH:
            return False
        
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        
        return has_upper and has_lower and has_digit
    
    def hash_password(self, password: str) -> str:
        """
        Hash password for secure storage.
        
        Args:
            password: Plain text password
            
        Returns:
            Hashed password string
        """
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register_user(
        self, 
        email: str, 
        password: str, 
        name: str,
        send_welcome: bool = True
    ) -> Dict:
        """
        Register a new user account.
        
        Args:
            email: User's email address
            password: User's password (will be hashed)
            name: User's display name
            send_welcome: Whether to send welcome email
            
        Returns:
            Dictionary containing user information
            
        Raises:
            UserValidationError: If validation fails
            DatabaseError: If database save fails
        """
        # Validate email
        if not self.validate_email(email):
            raise UserValidationError("Invalid email address")
        
        # Check if user already exists
        existing_user = self.db.get_user_by_email(email)
        if existing_user:
            raise UserValidationError("User with this email already exists")
        
        # Validate password
        if not self.validate_password(password):
            raise UserValidationError(
                "Password must be at least 8 characters with uppercase, "
                "lowercase, and numbers"
            )
        
        # Validate name
        if not name or len(name) > self.MAX_NAME_LENGTH:
            raise UserValidationError(
                f"Name must be between 1 and {self.MAX_NAME_LENGTH} characters"
            )
        
        # Create user record
        user_data = {
            'email': email.lower(),
            'password_hash': self.hash_password(password),
            'name': name.strip(),
            'created_at': datetime.now().isoformat(),
            'is_active': True,
            'failed_login_attempts': 0
        }
        
        # Save to database
        user_id = self.db.save_user(user_data)
        user_data['id'] = user_id
        
        # Send welcome email (best effort)
        if send_welcome:
            try:
                self.email_service.send_welcome_email(email, name)
            except Exception as e:
                # Log error but don't fail registration
                print(f"Failed to send welcome email: {e}")
        
        # Remove sensitive data before returning
        result = user_data.copy()
        del result['password_hash']
        
        return result
    
    def authenticate_user(self, email: str, password: str) -> Optional[Dict]:
        """
        Authenticate user with email and password.
        
        Args:
            email: User's email
            password: User's password
            
        Returns:
            User dictionary if authentication successful, None otherwise
        """
        if not email or not password:
            return None
        
        user = self.db.get_user_by_email(email.lower())
        if not user:
            return None
        
        # Check if account is locked
        if user.get('failed_login_attempts', 0) >= 5:
            return None
        
        # Verify password
        password_hash = self.hash_password(password)
        if password_hash != user['password_hash']:
            # Increment failed attempts
            user['failed_login_attempts'] = user.get('failed_login_attempts', 0) + 1
            self.db.update_user(user['id'], {
                'failed_login_attempts': user['failed_login_attempts']
            })
            return None
        
        # Reset failed attempts on successful login
        if user.get('failed_login_attempts', 0) > 0:
            self.db.update_user(user['id'], {'failed_login_attempts': 0})
        
        # Update last login
        self.db.update_user(user['id'], {
            'last_login': datetime.now().isoformat()
        })
        
        # Return user without sensitive data
        result = user.copy()
        del result['password_hash']
        return result
    
    def update_profile(self, user_id: int, updates: Dict) -> bool:
        """
        Update user profile information.
        
        Args:
            user_id: ID of user to update
            updates: Dictionary of fields to update
            
        Returns:
            True if update successful, False otherwise
        """
        user = self.db.get_user_by_id(user_id)
        if not user:
            return False
        
        # Don't allow updating sensitive fields
        sensitive_fields = {'password_hash', 'id', 'created_at', 'failed_login_attempts'}
        safe_updates = {k: v for k, v in updates.items() if k not in sensitive_fields}
        
        # Validate name if provided
        if 'name' in safe_updates:
            if len(safe_updates['name']) > self.MAX_NAME_LENGTH:
                raise UserValidationError(
                    f"Name must be less than {self.MAX_NAME_LENGTH} characters"
                )
        
        return self.db.update_user(user_id, safe_updates)
    
    def deactivate_account(self, user_id: int) -> bool:
        """
        Deactivate a user account.
        
        Args:
            user_id: ID of user to deactivate
            
        Returns:
            True if deactivation successful
        """
        return self.db.update_user(user_id, {
            'is_active': False,
            'deactivated_at': datetime.now().isoformat()
        })
    
    def get_user_stats(self, user_id: int) -> Optional[Dict]:
        """
        Get statistics about a user account.
        
        Args:
            user_id: User ID
            
        Returns:
            Dictionary with user stats or None if user not found
        """
        user = self.db.get_user_by_id(user_id)
        if not user:
            return None
        
        created_at = datetime.fromisoformat(user['created_at'])
        account_age_days = (datetime.now() - created_at).days
        
        return {
            'user_id': user_id,
            'name': user['name'],
            'email': user['email'],
            'account_age_days': account_age_days,
            'is_active': user.get('is_active', True),
            'last_login': user.get('last_login'),
            'created_at': user['created_at']
        }


def calculate_user_tier(account_age_days: int, purchase_count: int) -> str:
    """
    Calculate user loyalty tier based on activity.
    
    Args:
        account_age_days: Number of days since account creation
        purchase_count: Number of purchases made
        
    Returns:
        Tier name: "bronze", "silver", "gold", or "platinum"
    """
    if purchase_count >= 50 and account_age_days >= 365:
        return "platinum"
    elif purchase_count >= 20 or account_age_days >= 730:
        return "gold"
    elif purchase_count >= 5 or account_age_days >= 180:
        return "silver"
    else:
        return "bronze"
