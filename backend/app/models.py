from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Numeric, JSON
from app.database import Base


class User(Base):
    """User model"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    phone = Column(String(20))
    company_name = Column(String(255))
    address = Column(Text)
    city = Column(String(100))
    province = Column(String(100))
    postal_code = Column(String(20))
    country = Column(String(100))
    role = Column(String(50), default="customer")  # customer, admin
    status = Column(String(50), default="active")  # active, inactive, suspended
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<User {self.email}>"


class Service(Base):
    """Service/Product model"""
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    long_description = Column(Text)
    category = Column(String(100), index=True)
    price = Column(Numeric(10, 2))
    billing_period = Column(String(50))  # once, monthly, annual, custom
    image_url = Column(String(500))
    features = Column(JSON)
    is_available = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Service {self.name}>"


class Cart(Base):
    """Shopping cart model"""
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Cart {self.user_id}>"


class CartItem(Base):
    """Cart item model"""
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, index=True)
    cart_id = Column(Integer, nullable=False)
    service_id = Column(Integer, nullable=False)
    quantity = Column(Integer, default=1)
    added_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<CartItem {self.service_id}>"


class Order(Base):
    """Order model"""
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False)
    order_number = Column(String(50), unique=True, index=True)
    status = Column(String(50), default="pending")  # pending, processing, completed, cancelled
    total_amount = Column(Numeric(10, 2))
    payment_status = Column(String(50), default="pending")  # pending, paid, failed
    payment_method = Column(String(100))
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Order {self.order_number}>"


class OrderItem(Base):
    """Order item model"""
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, nullable=False)
    service_id = Column(Integer, nullable=False)
    service_name = Column(String(255))
    quantity = Column(Integer)
    price = Column(Numeric(10, 2))
    billing_period = Column(String(50))
    line_total = Column(Numeric(10, 2))
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<OrderItem {self.order_id}>"


class Invoice(Base):
    """Invoice model"""
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, nullable=False)
    invoice_number = Column(String(50), unique=True, index=True)
    amount = Column(Numeric(10, 2))
    status = Column(String(50), default="draft")  # draft, sent, paid, overdue
    issued_at = Column(DateTime)
    due_at = Column(DateTime)
    paid_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Invoice {self.invoice_number}>"


class Payment(Base):
    """Payment model"""
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, nullable=False)
    amount = Column(Numeric(10, 2))
    currency = Column(String(10), default="ZAR")
    payment_method = Column(String(100))  # stripe, payfast
    transaction_id = Column(String(255), unique=True)
    status = Column(String(50))  # pending, completed, failed
    metadata = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Payment {self.transaction_id}>"
