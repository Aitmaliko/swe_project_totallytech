from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Supplier, User, UserRole
from utils.security import get_current_active_user

router = APIRouter(prefix="/api/suppliers", tags=["Suppliers"])


@router.get("/")
def get_all_suppliers(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Получить список всех уникальных поставщиков (по company_name)"""
    # Получаем всех поставщиков
    suppliers = db.query(Supplier).all()
    
    # Группируем по company_name для получения уникальных компаний
    unique_suppliers = {}
    for supplier in suppliers:
        if supplier.company_name not in unique_suppliers:
            unique_suppliers[supplier.company_name] = {
                "id": supplier.id,
                "company_name": supplier.company_name,
                "company_address": supplier.company_address,
                "tax_id": supplier.tax_id,
                "description": supplier.description
            }
    
    return list(unique_suppliers.values())


@router.get("/{supplier_id}")
def get_supplier(
    supplier_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Получить информацию о конкретном поставщике"""
    supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
    
    if not supplier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Supplier not found"
        )
    
    return {
        "id": supplier.id,
        "company_name": supplier.company_name,
        "company_address": supplier.company_address,
        "tax_id": supplier.tax_id,
        "description": supplier.description
    }
