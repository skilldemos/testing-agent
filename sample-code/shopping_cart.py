"""
Shopping Cart Module

Manages shopping cart operations for e-commerce platform.
Demonstrates complex business logic that needs thorough testing.
"""

from typing import List, Dict, Optional
from decimal import Decimal
from datetime import datetime


class CartError(Exception):
    """Base exception for cart operations."""
    pass


class InvalidQuantityError(CartError):
    """Raised when quantity is invalid."""
    pass


class ProductNotFoundError(CartError):
    """Raised when product doesn't exist."""
    pass


class Product:
    """Product model."""
    
    def __init__(
        self,
        id: int,
        name: str,
        price: Decimal,
        stock: int,
        max_quantity: int = 10
    ):
        self.id = id
        self.name = name
        self.price = price
        self.stock = stock
        self.max_quantity = max_quantity


class CartItem:
    """Represents an item in the shopping cart."""
    
    def __init__(self, product: Product, quantity: int):
        if quantity <= 0:
            raise InvalidQuantityError("Quantity must be positive")
        if quantity > product.stock:
            raise InvalidQuantityError(f"Only {product.stock} items in stock")
        if quantity > product.max_quantity:
            raise InvalidQuantityError(
                f"Maximum {product.max_quantity} items per order"
            )
        
        self.product = product
        self.quantity = quantity
        self.added_at = datetime.now()
    
    def get_subtotal(self) -> Decimal:
        """Calculate subtotal for this cart item."""
        return self.product.price * self.quantity
    
    def to_dict(self) -> Dict:
        """Convert to dictionary representation."""
        return {
            'product_id': self.product.id,
            'product_name': self.product.name,
            'price': float(self.product.price),
            'quantity': self.quantity,
            'subtotal': float(self.get_subtotal()),
            'added_at': self.added_at.isoformat()
        }


class ShoppingCart:
    """
    Shopping cart that manages items and calculates totals.
    
    Features:
    - Add/remove items
    - Update quantities
    - Calculate totals with tax
    - Apply discount codes
    - Validate stock availability
    """
    
    TAX_RATE = Decimal('0.08')  # 8% sales tax
    FREE_SHIPPING_THRESHOLD = Decimal('50.00')
    SHIPPING_COST = Decimal('5.99')
    
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.items: List[CartItem] = []
        self.discount_code: Optional[str] = None
        self.discount_amount: Decimal = Decimal('0')
    
    def add_item(self, product: Product, quantity: int = 1) -> None:
        """
        Add a product to the cart.
        
        Args:
            product: Product to add
            quantity: Quantity to add
            
        Raises:
            InvalidQuantityError: If quantity is invalid
        """
        # Check if item already in cart
        for item in self.items:
            if item.product.id == product.id:
                # Update existing item
                new_quantity = item.quantity + quantity
                if new_quantity > product.stock:
                    raise InvalidQuantityError(f"Only {product.stock} items in stock")
                if new_quantity > product.max_quantity:
                    raise InvalidQuantityError(
                        f"Maximum {product.max_quantity} items per order"
                    )
                item.quantity = new_quantity
                return
        
        # Add new item
        cart_item = CartItem(product, quantity)
        self.items.append(cart_item)
    
    def remove_item(self, product_id: int) -> bool:
        """
        Remove a product from the cart.
        
        Args:
            product_id: ID of product to remove
            
        Returns:
            True if item was removed, False if not found
        """
        for i, item in enumerate(self.items):
            if item.product.id == product_id:
                self.items.pop(i)
                return True
        return False
    
    def update_quantity(self, product_id: int, quantity: int) -> bool:
        """
        Update quantity of a product in cart.
        
        Args:
            product_id: ID of product to update
            quantity: New quantity
            
        Returns:
            True if updated, False if product not in cart
            
        Raises:
            InvalidQuantityError: If quantity is invalid
        """
        if quantity <= 0:
            raise InvalidQuantityError("Quantity must be positive")
        
        for item in self.items:
            if item.product.id == product_id:
                if quantity > item.product.stock:
                    raise InvalidQuantityError(
                        f"Only {item.product.stock} items in stock"
                    )
                if quantity > item.product.max_quantity:
                    raise InvalidQuantityError(
                        f"Maximum {item.product.max_quantity} items per order"
                    )
                item.quantity = quantity
                return True
        
        return False
    
    def get_item_count(self) -> int:
        """Get total number of items in cart."""
        return sum(item.quantity for item in self.items)
    
    def get_subtotal(self) -> Decimal:
        """Calculate subtotal of all items."""
        return sum(item.get_subtotal() for item in self.items)
    
    def get_tax(self) -> Decimal:
        """Calculate tax amount."""
        taxable_amount = self.get_subtotal() - self.discount_amount
        return (taxable_amount * self.TAX_RATE).quantize(Decimal('0.01'))
    
    def get_shipping_cost(self) -> Decimal:
        """Calculate shipping cost."""
        subtotal = self.get_subtotal()
        if subtotal >= self.FREE_SHIPPING_THRESHOLD:
            return Decimal('0')
        return self.SHIPPING_COST
    
    def apply_discount_code(self, code: str, discount_pct: Decimal) -> bool:
        """
        Apply a discount code to the cart.
        
        Args:
            code: Discount code
            discount_pct: Discount percentage (0-100)
            
        Returns:
            True if discount applied
            
        Raises:
            ValueError: If discount percentage is invalid
        """
        if discount_pct < 0 or discount_pct > 100:
            raise ValueError("Discount percentage must be between 0 and 100")
        
        if not self.items:
            return False
        
        self.discount_code = code
        subtotal = self.get_subtotal()
        self.discount_amount = (subtotal * discount_pct / 100).quantize(Decimal('0.01'))
        return True
    
    def get_total(self) -> Decimal:
        """Calculate final total including tax and shipping."""
        subtotal = self.get_subtotal()
        discount = self.discount_amount
        tax = self.get_tax()
        shipping = self.get_shipping_cost()
        
        total = subtotal - discount + tax + shipping
        return total.quantize(Decimal('0.01'))
    
    def clear(self) -> None:
        """Remove all items from cart."""
        self.items = []
        self.discount_code = None
        self.discount_amount = Decimal('0')
    
    def to_dict(self) -> Dict:
        """Convert cart to dictionary representation."""
        return {
            'user_id': self.user_id,
            'items': [item.to_dict() for item in self.items],
            'item_count': self.get_item_count(),
            'subtotal': float(self.get_subtotal()),
            'discount_code': self.discount_code,
            'discount_amount': float(self.discount_amount),
            'tax': float(self.get_tax()),
            'shipping': float(self.get_shipping_cost()),
            'total': float(self.get_total())
        }
    
    def validate_stock(self, inventory: Dict[int, int]) -> List[str]:
        """
        Validate all items against current inventory.
        
        Args:
            inventory: Dictionary mapping product_id to available stock
            
        Returns:
            List of error messages for items with insufficient stock
        """
        errors = []
        for item in self.items:
            available = inventory.get(item.product.id, 0)
            if item.quantity > available:
                errors.append(
                    f"{item.product.name}: need {item.quantity}, "
                    f"only {available} available"
                )
        return errors
    
    def is_empty(self) -> bool:
        """Check if cart is empty."""
        return len(self.items) == 0
