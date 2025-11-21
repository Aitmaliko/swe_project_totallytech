from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from models import UserRole, LinkStatus, OrderStatus, ComplaintStatus, MessageType

# Auth Schemas
class UserBase(BaseModel):
    email: EmailStr
    phone: Optional[str] = None
    full_name: str
    role: UserRole

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    user_id: Optional[int] = None

# Supplier Schemas
class SupplierBase(BaseModel):
    company_name: str
    company_address: Optional[str] = None
    tax_id: Optional[str] = None
    description: Optional[str] = None

class SupplierCreate(BaseModel):
    user: UserCreate
    supplier_info: SupplierBase

class SupplierResponse(SupplierBase):
    id: int
    user_id: int
    created_at: datetime
    user: UserResponse
    
    class Config:
        from_attributes = True

# Consumer Schemas
class ConsumerBase(BaseModel):
    business_name: str
    business_type: Optional[str] = None
    address: Optional[str] = None

class ConsumerCreate(BaseModel):
    user: UserCreate
    consumer_info: ConsumerBase

class ConsumerResponse(ConsumerBase):
    id: int
    user_id: int
    created_at: datetime
    user: UserResponse
    
    class Config:
        from_attributes = True

# Link Schemas
class LinkCreate(BaseModel):
    supplier_id: int
    notes: Optional[str] = None

class LinkUpdate(BaseModel):
    status: LinkStatus
    notes: Optional[str] = None

class LinkResponse(BaseModel):
    id: int
    consumer_id: int
    supplier_id: int
    consumer_name: Optional[str] = None
    supplier_name: Optional[str] = None
    status: LinkStatus
    requested_at: datetime
    responded_at: Optional[datetime] = None
    notes: Optional[str] = None
    
    class Config:
        from_attributes = True

# Product Schemas
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    category: Optional[str] = None
    unit: str
    price: float
    stock_quantity: int = 0
    is_available: bool = True

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    unit: Optional[str] = None
    price: Optional[float] = None
    stock_quantity: Optional[int] = None
    is_available: Optional[bool] = None

class ProductResponse(ProductBase):
    id: int
    supplier_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    has_image: bool = False
    
    class Config:
        from_attributes = True

# Order Schemas
class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int

class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    unit_price: float
    total_price: float
    
    class Config:
        from_attributes = True

class OrderCreate(BaseModel):
    supplier_id: int
    items: List[OrderItemCreate]
    notes: Optional[str] = None

class OrderUpdate(BaseModel):
    status: OrderStatus
    notes: Optional[str] = None

class OrderResponse(BaseModel):
    id: int
    consumer_id: int
    supplier_id: int
    status: OrderStatus
    total_amount: float
    notes: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    items: List[OrderItemResponse] = []
    
    class Config:
        from_attributes = True

# Message Schemas
class MessageCreate(BaseModel):
    link_id: int
    message_type: MessageType = MessageType.TEXT
    content: Optional[str] = None

class MessageResponse(BaseModel):
    id: int
    link_id: int
    sender_id: int
    message_type: MessageType
    content: Optional[str] = None
    file_name: Optional[str] = None
    file_mime_type: Optional[str] = None
    is_read: bool
    created_at: datetime
    has_file: bool = False
    
    class Config:
        from_attributes = True

class ComplaintCreate(BaseModel):
    order_id: Optional[int] = None
    link_id: int
    title: str
    description: str
    priority: str = "normal"

class ComplaintUpdate(BaseModel):
    status: Optional[ComplaintStatus] = None
    assigned_to_id: Optional[int] = None
    resolution_notes: Optional[str] = None

class ComplaintResponse(BaseModel):
    id: int
    order_id: Optional[int] = None
    link_id: int
    created_by_id: int
    assigned_to_id: Optional[int] = None
    title: str
    description: str
    status: ComplaintStatus
    priority: str
    resolution_notes: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
