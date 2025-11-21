from __future__ import annotations
from sqlalchemy.orm import Session
from models import User, UserRole, Supplier, Consumer
from fastapi import HTTPException, status

def check_permission(current_user: User, required_roles: list[UserRole]):
    """Проверка прав доступа"""
    if current_user.role not in required_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to perform this action"
        )

def get_supplier_id(current_user: User, db: Session) -> int:
    """Получение supplier_id для текущего пользователя"""
    if current_user.role in [UserRole.OWNER, UserRole.MANAGER, UserRole.SALES]:
        # Получаем первую запись Supplier для этого пользователя
        supplier = db.query(Supplier).filter(Supplier.user_id == current_user.id).first()
        if supplier:
            return supplier.id
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Only supplier users can perform this action"
    )

def get_consumer_id(current_user: User, db: Session) -> int:
    """Получение consumer_id для текущего пользователя"""
    if current_user.role == UserRole.CONSUMER:
        consumer = db.query(Consumer).filter(Consumer.user_id == current_user.id).first()
        if consumer:
            return consumer.id
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Only consumer users can perform this action"
    )
