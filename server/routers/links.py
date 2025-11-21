from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from database import get_db
from models import User, Link, LinkStatus, UserRole, Supplier, Consumer
from schemas import LinkCreate, LinkUpdate, LinkResponse
from utils.security import get_current_active_user
from utils.permissions import get_consumer_id, get_supplier_id

router = APIRouter(prefix="/api/links", tags=["Links"])

def enrich_link_with_names(link: Link, db: Session) -> dict:
    """Добавить имена consumer и supplier к link"""
    link_dict = {
        "id": link.id,
        "consumer_id": link.consumer_id,
        "supplier_id": link.supplier_id,
        "status": link.status,
        "requested_at": link.requested_at,
        "responded_at": link.responded_at,
        "notes": link.notes,
        "consumer_name": None,
        "supplier_name": None
    }
    
    # Получаем имя consumer
    consumer = db.query(Consumer).filter(Consumer.id == link.consumer_id).first()
    if consumer:
        link_dict["consumer_name"] = consumer.business_name
    
    # Получаем имя supplier (company_name)
    supplier = db.query(Supplier).filter(Supplier.id == link.supplier_id).first()
    if supplier:
        link_dict["supplier_name"] = supplier.company_name
    
    return link_dict

@router.post("/request", response_model=LinkResponse, status_code=status.HTTP_201_CREATED)
def request_link(
    link_data: LinkCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Consumer отправляет запрос на связь с Supplier"""
    consumer_id = get_consumer_id(current_user, db)
    
    # Проверка существования поставщика
    supplier = db.query(Supplier).filter(Supplier.id == link_data.supplier_id).first()
    if not supplier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Supplier with id {link_data.supplier_id} not found"
        )
    
    # Проверка существующей связи
    existing_link = db.query(Link).filter(
        Link.consumer_id == consumer_id,
        Link.supplier_id == link_data.supplier_id
    ).first()
    
    if existing_link:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Link request already exists"
        )
    
    # Создание запроса на связь
    link = Link(
        consumer_id=consumer_id,
        supplier_id=link_data.supplier_id,
        status=LinkStatus.PENDING,
        notes=link_data.notes or ""
    )
    db.add(link)
    db.commit()
    db.refresh(link)
    
    # Обогащаем результат именами
    return enrich_link_with_names(link, db)

@router.get("/pending")
def get_pending_links(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Получить все ожидающие запросы (для Supplier)"""
    # Получаем company_name текущего пользователя
    supplier_record = db.query(Supplier).filter(Supplier.user_id == current_user.id).first()
    if not supplier_record:
        return []
    
    company_name = supplier_record.company_name
    
    # Находим все записи Supplier с таким же company_name
    supplier_ids = db.query(Supplier.id).filter(Supplier.company_name == company_name).all()
    supplier_ids = [sid[0] for sid in supplier_ids]
    
    # Получаем pending links для всех supplier_id с этим company_name
    links = db.query(Link).filter(
        Link.supplier_id.in_(supplier_ids),
        Link.status == LinkStatus.PENDING
    ).all()
    
    # Обогащаем каждый link именами
    result = []
    for link in links:
        enriched = enrich_link_with_names(link, db)
        result.append(enriched)
    
    return result

@router.get("/my-links")
def get_my_links(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Получить все связи текущего пользователя"""
    if current_user.role == UserRole.CONSUMER:
        consumer_id = get_consumer_id(current_user, db)
        links = db.query(Link).filter(Link.consumer_id == consumer_id).all()
    else:
        # Получаем company_name текущего пользователя
        supplier_record = db.query(Supplier).filter(Supplier.user_id == current_user.id).first()
        if not supplier_record:
            return []
        
        company_name = supplier_record.company_name
        
        # Находим все записи Supplier с таким же company_name
        supplier_ids = db.query(Supplier.id).filter(Supplier.company_name == company_name).all()
        supplier_ids = [sid[0] for sid in supplier_ids]
        
        # Получаем links для всех supplier_id с этим company_name
        links = db.query(Link).filter(Link.supplier_id.in_(supplier_ids)).all()
    
    # Обогащаем каждый link именами
    result = []
    for link in links:
        enriched = enrich_link_with_names(link, db)
        result.append(enriched)
    
    return result

@router.put("/{link_id}", response_model=LinkResponse)
def update_link_status(
    link_id: int,
    link_update: LinkUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Обновить статус связи (принять/отклонить) - для Supplier (Owner/Manager/Sales)"""
    # Sales Representative может принимать/отклонять link requests
    if current_user.role not in [UserRole.OWNER, UserRole.MANAGER, UserRole.SALES]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only Supplier staff can update link status"
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
    
    # Ищем link среди supplier_id с этим company_name
    link = db.query(Link).filter(
        Link.id == link_id,
        Link.supplier_id.in_(supplier_ids)
    ).first()
    
    if not link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Link not found"
        )
    
    link.status = link_update.status
    if link_update.notes:
        link.notes = link_update.notes
    link.responded_at = datetime.utcnow()
    
    db.commit()
    db.refresh(link)
    
    return link

@router.get("/accepted")
def get_accepted_links(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Получить все принятые связи"""
    if current_user.role == UserRole.CONSUMER:
        consumer_id = get_consumer_id(current_user, db)
        links = db.query(Link).filter(
            Link.consumer_id == consumer_id,
            Link.status == LinkStatus.ACCEPTED
        ).all()
    else:
        # Получаем company_name текущего пользователя
        supplier_record = db.query(Supplier).filter(Supplier.user_id == current_user.id).first()
        if not supplier_record:
            return []
        
        company_name = supplier_record.company_name
        
        # Находим все записи Supplier с таким же company_name
        supplier_ids = db.query(Supplier.id).filter(Supplier.company_name == company_name).all()
        supplier_ids = [sid[0] for sid in supplier_ids]
        
        # Получаем accepted links для всех supplier_id с этим company_name
        links = db.query(Link).filter(
            Link.supplier_id.in_(supplier_ids),
            Link.status == LinkStatus.ACCEPTED
        ).all()
    
    # Обогащаем каждый link именами
    result = []
    for link in links:
        enriched = enrich_link_with_names(link, db)
        result.append(enriched)
    
    return result

@router.delete("/{link_id}")
def block_link(
    link_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Заблокировать связь - только для Supplier (Owner/Manager)"""
    if current_user.role not in [UserRole.OWNER, UserRole.MANAGER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only Owner or Manager can block links"
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
    
    # Ищем link среди supplier_id с этим company_name
    link = db.query(Link).filter(
        Link.id == link_id,
        Link.supplier_id.in_(supplier_ids)
    ).first()
    
    if not link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Link not found"
        )
    
    link.status = LinkStatus.BLOCKED
    db.commit()
    
    return {"message": "Link blocked successfully"}
