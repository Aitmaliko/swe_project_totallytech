from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import User, Order, OrderItem, Product, Link, LinkStatus, OrderStatus, UserRole, Supplier
from schemas import OrderCreate, OrderUpdate, OrderResponse
from utils.security import get_current_active_user
from utils.permissions import get_consumer_id, get_supplier_id

router = APIRouter(prefix="/api/orders", tags=["Orders"])

@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(
    order_data: OrderCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Создать заказ - только для Consumer"""
    consumer_id = get_consumer_id(current_user, db)
    
    # Проверяем наличие принятой связи
    link = db.query(Link).filter(
        Link.consumer_id == consumer_id,
        Link.supplier_id == order_data.supplier_id,
        Link.status == LinkStatus.ACCEPTED
    ).first()
    
    if not link:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You must have an accepted link with this supplier to create orders"
        )
    
    # Проверяем доступность всех продуктов и вычисляем сумму
    total_amount = 0
    order_items_data = []
    
    for item in order_data.items:
        product = db.query(Product).filter(
            Product.id == item.product_id,
            Product.supplier_id == order_data.supplier_id,
            Product.is_available == True
        ).first()
        
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product {item.product_id} not found or not available"
            )
        
        if product.stock_quantity < item.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient stock for product {product.name}"
            )
        
        item_total = float(product.price) * item.quantity
        total_amount += item_total
        
        order_items_data.append({
            "product_id": product.id,
            "quantity": item.quantity,
            "unit_price": product.price,
            "total_price": item_total
        })
    
    # Создаем заказ
    order = Order(
        consumer_id=consumer_id,
        supplier_id=order_data.supplier_id,
        status=OrderStatus.PENDING,
        total_amount=total_amount,
        notes=order_data.notes
    )
    db.add(order)
    db.flush()
    
    # Создаем items заказа
    for item_data in order_items_data:
        order_item = OrderItem(
            order_id=order.id,
            **item_data
        )
        db.add(order_item)
    
    db.commit()
    db.refresh(order)
    
    return order

@router.get("/my-orders", response_model=List[OrderResponse])
def get_my_orders(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Получить свои заказы"""
    if current_user.role == UserRole.CONSUMER:
        consumer_id = get_consumer_id(current_user, db)
        orders = db.query(Order).filter(Order.consumer_id == consumer_id).all()
    else:
        # Получаем company_name текущего пользователя
        supplier_record = db.query(Supplier).filter(Supplier.user_id == current_user.id).first()
        if not supplier_record:
            return []
        
        company_name = supplier_record.company_name
        
        # Находим все записи Supplier с таким же company_name
        supplier_ids = db.query(Supplier.id).filter(Supplier.company_name == company_name).all()
        supplier_ids = [sid[0] for sid in supplier_ids]
        
        # Получаем заказы для всех supplier_id с этим company_name
        orders = db.query(Order).filter(Order.supplier_id.in_(supplier_ids)).all()
    
    return orders

@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Получить детали заказа"""
    order = db.query(Order).filter(Order.id == order_id).first()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    # Проверяем доступ
    if current_user.role == UserRole.CONSUMER:
        consumer_id = get_consumer_id(current_user, db)
        if order.consumer_id != consumer_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    else:
        # Получаем company_name текущего пользователя
        supplier_record = db.query(Supplier).filter(Supplier.user_id == current_user.id).first()
        if not supplier_record:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        
        company_name = supplier_record.company_name
        
        # Находим все записи Supplier с таким же company_name
        supplier_ids = db.query(Supplier.id).filter(Supplier.company_name == company_name).all()
        supplier_ids = [sid[0] for sid in supplier_ids]
        
        # Проверяем что заказ принадлежит нашей компании
        if order.supplier_id not in supplier_ids:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
    return order

@router.put("/{order_id}", response_model=OrderResponse)
def update_order_status(
    order_id: int,
    order_update: OrderUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Обновить статус заказа - для Supplier"""
    # Получаем company_name текущего пользователя
    supplier_record = db.query(Supplier).filter(Supplier.user_id == current_user.id).first()
    if not supplier_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Supplier record not found"
        )
    
    company_name = supplier_record.company_name
    
    # Находим все записи Supplier с таким же company_name
    supplier_ids = db.query(Supplier.id).filter(Supplier.company_name == company_name).all()
    supplier_ids = [sid[0] for sid in supplier_ids]
    
    # Ищем заказ среди supplier_id с этим company_name
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.supplier_id.in_(supplier_ids)
    ).first()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    # Обновляем статус
    order.status = order_update.status
    if order_update.notes:
        order.notes = order_update.notes
    
    # Если заказ принят, уменьшаем stock
    if order_update.status == OrderStatus.ACCEPTED and order.status == OrderStatus.PENDING:
        for item in order.items:
            product = db.query(Product).filter(Product.id == item.product_id).first()
            if product:
                product.stock_quantity -= item.quantity
    
    db.commit()
    db.refresh(order)
    
    return order

@router.get("/pending/list", response_model=List[OrderResponse])
def get_pending_orders(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Получить все ожидающие заказы - для Supplier"""
    # Получаем company_name текущего пользователя
    supplier_record = db.query(Supplier).filter(Supplier.user_id == current_user.id).first()
    if not supplier_record:
        return []
    
    company_name = supplier_record.company_name
    
    # Находим все записи Supplier с таким же company_name
    supplier_ids = db.query(Supplier.id).filter(Supplier.company_name == company_name).all()
    supplier_ids = [sid[0] for sid in supplier_ids]
    
    # Получаем pending заказы для всех supplier_id с этим company_name
    orders = db.query(Order).filter(
        Order.supplier_id.in_(supplier_ids),
        Order.status == OrderStatus.PENDING
    ).all()
    
    return orders

@router.delete("/{order_id}")
def cancel_order(
    order_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Отменить заказ - Consumer может отменить только PENDING заказы"""
    if current_user.role == UserRole.CONSUMER:
        consumer_id = get_consumer_id(current_user, db)
        
        order = db.query(Order).filter(
            Order.id == order_id,
            Order.consumer_id == consumer_id,
            Order.status == OrderStatus.PENDING
        ).first()
        
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found or cannot be cancelled"
            )
        
        order.status = OrderStatus.CANCELLED
        db.commit()
        
        return {"message": "Order cancelled successfully"}
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only consumers can cancel orders"
        )
