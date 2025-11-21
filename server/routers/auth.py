from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import User, Supplier, Consumer, UserRole
from schemas import (
    UserCreate, UserResponse, Token, SupplierCreate, 
    ConsumerCreate, SupplierResponse, ConsumerResponse
)
from utils.security import (
    verify_password, get_password_hash, 
    create_access_token, create_refresh_token,
    get_current_active_user
)

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/register/supplier", response_model=SupplierResponse, status_code=status.HTTP_201_CREATED)
def register_supplier(supplier_data: SupplierCreate, db: Session = Depends(get_db)):
    """Регистрация поставщика (Owner)"""
    # Проверка существования пользователя
    existing_user = db.query(User).filter(
        (User.email == supplier_data.user.email) | 
        (User.phone == supplier_data.user.phone)
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email or phone already exists"
        )
    
    # Создание пользователя
    user = User(
        email=supplier_data.user.email,
        phone=supplier_data.user.phone,
        full_name=supplier_data.user.full_name,
        hashed_password=get_password_hash(supplier_data.user.password),
        role=UserRole.OWNER  # По умолчанию Owner при регистрации поставщика
    )
    db.add(user)
    db.flush()
    
    # Создание поставщика
    supplier = Supplier(
        user_id=user.id,
        company_name=supplier_data.supplier_info.company_name,
        company_address=supplier_data.supplier_info.company_address,
        tax_id=supplier_data.supplier_info.tax_id,
        description=supplier_data.supplier_info.description
    )
    db.add(supplier)
    db.commit()
    db.refresh(supplier)
    
    return supplier

@router.post("/register/consumer", response_model=ConsumerResponse, status_code=status.HTTP_201_CREATED)
def register_consumer(consumer_data: ConsumerCreate, db: Session = Depends(get_db)):
    """Регистрация потребителя (ресторан/отель)"""
    # Проверка существования пользователя
    existing_user = db.query(User).filter(
        (User.email == consumer_data.user.email) | 
        (User.phone == consumer_data.user.phone)
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email or phone already exists"
        )
    
    # Создание пользователя
    user = User(
        email=consumer_data.user.email,
        phone=consumer_data.user.phone,
        full_name=consumer_data.user.full_name,
        hashed_password=get_password_hash(consumer_data.user.password),
        role=UserRole.CONSUMER
    )
    db.add(user)
    db.flush()
    
    # Создание потребителя
    consumer = Consumer(
        user_id=user.id,
        business_name=consumer_data.consumer_info.business_name,
        business_type=consumer_data.consumer_info.business_type,
        address=consumer_data.consumer_info.address
    )
    db.add(consumer)
    db.commit()
    db.refresh(consumer)
    
    return consumer

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Вход в систему"""
    user = db.query(User).filter(User.email == form_data.username).first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    # Создание токенов
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_active_user)):
    """Получение информации о текущем пользователе"""
    return current_user

@router.post("/create-staff", response_model=UserResponse)
def create_staff_member(
    user_data: UserCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Создание сотрудника (Manager или Sales) - только для Owner"""
    if current_user.role != UserRole.OWNER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only Owner can create staff members"
        )
    
    if user_data.role not in [UserRole.MANAGER, UserRole.SALES]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can only create Manager or Sales roles"
        )
    
    # Проверка существования пользователя
    existing_user = db.query(User).filter(
        (User.email == user_data.email) | (User.phone == user_data.phone)
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email or phone already exists"
        )
    
    # Создание пользователя
    user = User(
        email=user_data.email,
        phone=user_data.phone,
        full_name=user_data.full_name,
        hashed_password=get_password_hash(user_data.password),
        role=user_data.role
    )
    db.add(user)
    db.flush()
    
    # Связываем с тем же поставщиком что у Owner
    if current_user.supplier:
        supplier = Supplier(
            user_id=user.id,
            company_name=current_user.supplier.company_name,
            company_address=current_user.supplier.company_address,
            tax_id=current_user.supplier.tax_id,
            description=current_user.supplier.description
        )
        db.add(supplier)
    
    db.commit()
    db.refresh(user)
    
    return user

@router.get("/staff", response_model=List[UserResponse])
def get_staff_members(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Получить список сотрудников - только для Owner"""
    if current_user.role != UserRole.OWNER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only Owner can view staff members"
        )
    
    if not current_user.supplier:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Supplier not found"
        )
    
    # Получаем company_name текущего Owner
    company_name = current_user.supplier.company_name
    
    # Находим всех пользователей с таким же company_name
    staff = db.query(User).join(Supplier).filter(
        Supplier.company_name == company_name,
        User.role.in_([UserRole.MANAGER, UserRole.SALES])
    ).all()
    
    return staff

@router.delete("/staff/{user_id}")
def delete_staff_member(
    user_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Удалить сотрудника (Manager или Sales) - только для Owner"""
    if current_user.role != UserRole.OWNER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only Owner can delete staff members"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if user.role not in [UserRole.MANAGER, UserRole.SALES]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can only delete Manager or Sales roles"
        )
    
    # Проверяем что это сотрудник того же supplier
    if user.supplier and current_user.supplier:
        if user.supplier.company_name != current_user.supplier.company_name:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot delete staff from another supplier"
            )
    
    # Деактивируем пользователя вместо физического удаления
    user.is_active = False
    db.commit()
    
    return {"message": "Staff member deleted successfully"}

@router.delete("/account")
def deactivate_account(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Деактивировать аккаунт supplier - только для Owner"""
    if current_user.role != UserRole.OWNER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only Owner can deactivate supplier account"
        )
    
    if not current_user.supplier:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Supplier not found"
        )
    
    # Деактивируем owner и всех его staff
    supplier_id = current_user.supplier.id
    
    # Деактивируем всех пользователей supplier
    users = db.query(User).join(Supplier).filter(Supplier.id == supplier_id).all()
    
    for user in users:
        user.is_active = False
    
    db.commit()
    
    return {"message": "Supplier account deactivated successfully"}
