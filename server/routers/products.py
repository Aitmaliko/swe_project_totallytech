from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models import User, Product, Link, LinkStatus, UserRole, Supplier
from schemas import ProductCreate, ProductUpdate, ProductResponse
from utils.security import get_current_active_user
from utils.permissions import get_supplier_id, get_consumer_id

router = APIRouter(prefix="/api/products", tags=["Products"])

@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    product_data: ProductCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Создать продукт - только для Owner/Manager"""
    if current_user.role not in [UserRole.OWNER, UserRole.MANAGER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only Owner or Manager can create products"
        )
    
    supplier_id = get_supplier_id(current_user, db)
    
    product = Product(
        supplier_id=supplier_id,
        name=product_data.name,
        description=product_data.description,
        category=product_data.category,
        unit=product_data.unit,
        price=product_data.price,
        stock_quantity=product_data.stock_quantity,
        is_available=product_data.is_available
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    
    # Добавляем поле has_image
    product_dict = ProductResponse.from_orm(product)
    return product_dict

@router.post("/{product_id}/image")
def upload_product_image(
    product_id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Загрузить изображение продукта"""
    if current_user.role not in [UserRole.OWNER, UserRole.MANAGER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only Owner or Manager can upload images"
        )
    
    supplier_id = get_supplier_id(current_user, db)
    
    product = db.query(Product).filter(
        Product.id == product_id,
        Product.supplier_id == supplier_id
    ).first()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    # Читаем файл и сохраняем в BYTEA
    image_data = file.file.read()
    product.image_data = image_data
    
    db.commit()
    
    return {"message": "Image uploaded successfully"}

@router.get("/{product_id}/image")
def get_product_image(
    product_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Получить изображение продукта"""
    from fastapi.responses import Response
    
    product = db.query(Product).filter(Product.id == product_id).first()
    
    if not product or not product.image_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found"
        )
    
    return Response(content=product.image_data, media_type="image/jpeg")

@router.get("/supplier/{supplier_id}", response_model=List[ProductResponse])
def get_supplier_products(
    supplier_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Получить продукты поставщика - только для связанных Consumer или самого Supplier"""
    
    # Если текущий пользователь - Consumer, проверяем наличие связи
    if current_user.role == UserRole.CONSUMER:
        consumer_id = get_consumer_id(current_user, db)
        
        # Проверяем наличие принятой связи
        link = db.query(Link).filter(
            Link.consumer_id == consumer_id,
            Link.supplier_id == supplier_id,
            Link.status == LinkStatus.ACCEPTED
        ).first()
        
        if not link:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You must have an accepted link with this supplier to view products"
            )
    
    # Получаем продукты
    products = db.query(Product).filter(
        Product.supplier_id == supplier_id,
        Product.is_available == True
    ).all()
    
    # Преобразуем в response модель
    result = []
    for product in products:
        product_dict = ProductResponse.from_orm(product)
        product_dict.has_image = product.image_data is not None
        result.append(product_dict)
    
    return result

@router.get("/my-products", response_model=List[ProductResponse])
def get_my_products(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Получить свои продукты - для Supplier"""
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
    
    # Получаем продукты для всех supplier_id с этим company_name
    products = db.query(Product).filter(Product.supplier_id.in_(supplier_ids)).all()
    
    result = []
    for product in products:
        product_dict = ProductResponse.from_orm(product)
        product_dict.has_image = product.image_data is not None
        result.append(product_dict)
    
    return result

@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product_update: ProductUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Обновить продукт - только для Owner/Manager"""
    if current_user.role not in [UserRole.OWNER, UserRole.MANAGER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only Owner or Manager can update products"
        )
    
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
    
    # Ищем продукт среди supplier_id с этим company_name
    product = db.query(Product).filter(
        Product.id == product_id,
        Product.supplier_id.in_(supplier_ids)
    ).first()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    # Обновляем только переданные поля
    update_data = product_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(product, field, value)
    
    db.commit()
    db.refresh(product)
    
    product_dict = ProductResponse.from_orm(product)
    product_dict.has_image = product.image_data is not None
    
    return product_dict

@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Удалить продукт (мягкое удаление) - для Owner/Manager"""
    if current_user.role not in [UserRole.OWNER, UserRole.MANAGER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only Owner or Manager can delete products"
        )
    
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
    
    # Ищем продукт среди supplier_id с этим company_name
    product = db.query(Product).filter(
        Product.id == product_id,
        Product.supplier_id.in_(supplier_ids)
    ).first()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    # Мягкое удаление - делаем недоступным
    product.is_available = False
    db.commit()
    
    return {"message": "Product deleted successfully"}
