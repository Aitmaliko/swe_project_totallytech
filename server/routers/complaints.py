from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from database import get_db
from models import User, Complaint, Link, LinkStatus, ComplaintStatus, UserRole, Supplier
from schemas import ComplaintCreate, ComplaintUpdate, ComplaintResponse
from utils.security import get_current_active_user
from utils.permissions import get_consumer_id, get_supplier_id

router = APIRouter(prefix="/api/complaints", tags=["Complaints"])

@router.post("/", response_model=ComplaintResponse, status_code=status.HTTP_201_CREATED)
def create_complaint(
    complaint_data: ComplaintCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Создать жалобу - только Consumer для delivered orders"""
    
    # Только Consumer может создавать жалобы
    if current_user.role != UserRole.CONSUMER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only Consumer can create complaints"
        )
    
    consumer_id = get_consumer_id(current_user, db)
    
    # Проверяем доступ к link
    link = db.query(Link).filter(Link.id == complaint_data.link_id).first()
    
    if not link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Link not found"
        )
    
    if link.status != LinkStatus.ACCEPTED:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Link must be accepted to create complaints"
        )
    
    if link.consumer_id != consumer_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
    # Если order_id указан, проверяем что заказ существует и доставлен
    if complaint_data.order_id:
        from models import Order, OrderStatus
        order = db.query(Order).filter(
            Order.id == complaint_data.order_id,
            Order.consumer_id == consumer_id
        ).first()
        
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )
        
        # Жалобу по заказу можно создать только для доставленного заказа
        if order.status != OrderStatus.DELIVERED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Complaints can only be created for delivered orders"
            )
    
    complaint = Complaint(
        order_id=complaint_data.order_id,
        link_id=complaint_data.link_id,
        created_by_id=current_user.id,
        title=complaint_data.title,
        description=complaint_data.description,
        priority=complaint_data.priority,
        status=ComplaintStatus.OPEN
    )
    
    # Автоматически назначаем на Sales Representative
    # Находим Sales для этого supplier
    from models import Supplier
    sales = db.query(User).join(Supplier).filter(
        Supplier.id == link.supplier_id,
        User.role == UserRole.SALES
    ).first()
    
    if sales:
        complaint.assigned_to_id = sales.id
        complaint.status = ComplaintStatus.IN_PROGRESS
    
    db.add(complaint)
    db.commit()
    db.refresh(complaint)
    
    return complaint

@router.get("/my-complaints", response_model=List[ComplaintResponse])
def get_my_complaints(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Получить свои жалобы"""
    
    if current_user.role == UserRole.CONSUMER:
        # Consumer видит созданные им жалобы
        complaints = db.query(Complaint).filter(
            Complaint.created_by_id == current_user.id
        ).all()
    
    elif current_user.role == UserRole.SALES:
        # Sales видит назначенные на него жалобы
        complaints = db.query(Complaint).filter(
            Complaint.assigned_to_id == current_user.id
        ).all()
    
    elif current_user.role in [UserRole.OWNER, UserRole.MANAGER]:
        # Owner/Manager видят все жалобы своего supplier
        # Получаем company_name текущего пользователя
        supplier_record = db.query(Supplier).filter(Supplier.user_id == current_user.id).first()
        if not supplier_record:
            complaints = []
        else:
            company_name = supplier_record.company_name
            
            # Находим все записи Supplier с таким же company_name
            supplier_ids = db.query(Supplier.id).filter(Supplier.company_name == company_name).all()
            supplier_ids = [sid[0] for sid in supplier_ids]
            
            # Получаем все links для всех supplier_id с этим company_name
            links = db.query(Link).filter(Link.supplier_id.in_(supplier_ids)).all()
            link_ids = [link.id for link in links]
            
            complaints = db.query(Complaint).filter(
                Complaint.link_id.in_(link_ids)
            ).all()
    
    else:
        complaints = []
    
    return complaints

@router.get("/{complaint_id}", response_model=ComplaintResponse)
def get_complaint(
    complaint_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Получить детали жалобы"""
    complaint = db.query(Complaint).filter(Complaint.id == complaint_id).first()
    
    if not complaint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Complaint not found"
        )
    
    # Проверяем доступ
    link = complaint.link
    
    if current_user.role == UserRole.CONSUMER:
        consumer_id = get_consumer_id(current_user, db)
        if link.consumer_id != consumer_id:
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
        
        # Проверяем что link принадлежит нашей компании
        if link.supplier_id not in supplier_ids:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
    return complaint

@router.put("/{complaint_id}", response_model=ComplaintResponse)
def update_complaint(
    complaint_id: int,
    complaint_update: ComplaintUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Обновить жалобу"""
    complaint = db.query(Complaint).filter(Complaint.id == complaint_id).first()
    
    if not complaint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Complaint not found"
        )
    
    # Sales может обновить только назначенные на него жалобы
    if current_user.role == UserRole.SALES:
        if complaint.assigned_to_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only update complaints assigned to you"
            )
    
    # Manager/Owner могут обновить любые жалобы своего supplier
    elif current_user.role in [UserRole.OWNER, UserRole.MANAGER]:
        # Получаем company_name текущего пользователя
        supplier_record = db.query(Supplier).filter(Supplier.user_id == current_user.id).first()
        if not supplier_record:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        
        company_name = supplier_record.company_name
        
        # Находим все записи Supplier с таким же company_name
        supplier_ids = db.query(Supplier.id).filter(Supplier.company_name == company_name).all()
        supplier_ids = [sid[0] for sid in supplier_ids]
        
        # Проверяем что complaint.link принадлежит нашей компании
        if complaint.link.supplier_id not in supplier_ids:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only Sales/Manager/Owner can update complaints"
        )
    
    # Обновляем поля
    if complaint_update.status:
        complaint.status = complaint_update.status
        if complaint_update.status == ComplaintStatus.RESOLVED:
            complaint.resolved_at = datetime.utcnow()
    
    if complaint_update.assigned_to_id:
        complaint.assigned_to_id = complaint_update.assigned_to_id
    
    if complaint_update.resolution_notes:
        complaint.resolution_notes = complaint_update.resolution_notes
    
    db.commit()
    db.refresh(complaint)
    
    return complaint

@router.post("/{complaint_id}/escalate", response_model=ComplaintResponse)
def escalate_complaint(
    complaint_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Эскалировать жалобу от Sales к Manager"""
    
    if current_user.role != UserRole.SALES:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only Sales can escalate complaints"
        )
    
    complaint = db.query(Complaint).filter(
        Complaint.id == complaint_id,
        Complaint.assigned_to_id == current_user.id
    ).first()
    
    if not complaint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Complaint not found or not assigned to you"
        )
    
    # Находим Manager того же supplier (по company_name)
    # Получаем company_name текущего пользователя
    supplier_record = db.query(Supplier).filter(Supplier.user_id == current_user.id).first()
    if not supplier_record:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Supplier record not found"
        )
    
    company_name = supplier_record.company_name
    
    # Ищем Manager или Owner для эскалации (с тем же company_name)
    manager = db.query(User).join(Supplier).filter(
        Supplier.company_name == company_name,
        User.role.in_([UserRole.MANAGER, UserRole.OWNER])
    ).first()
    
    if not manager:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No Manager found for escalation"
        )
    
    complaint.status = ComplaintStatus.ESCALATED
    complaint.assigned_to_id = manager.id
    
    db.commit()
    db.refresh(complaint)
    
    return complaint

@router.get("/open/list", response_model=List[ComplaintResponse])
def get_open_complaints(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Получить все открытые жалобы - для Manager/Owner/Sales"""
    
    if current_user.role not in [UserRole.OWNER, UserRole.MANAGER, UserRole.SALES]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only Owner, Manager or Sales can view open complaints"
        )
    
    # Получаем company_name текущего пользователя
    supplier_record = db.query(Supplier).filter(Supplier.user_id == current_user.id).first()
    if not supplier_record:
        return []
    
    company_name = supplier_record.company_name
    
    # Находим все записи Supplier с таким же company_name
    supplier_ids = db.query(Supplier.id).filter(Supplier.company_name == company_name).all()
    supplier_ids = [sid[0] for sid in supplier_ids]
    
    # Получаем все links для всех supplier_id с этим company_name
    links = db.query(Link).filter(Link.supplier_id.in_(supplier_ids)).all()
    link_ids = [link.id for link in links]
    
    complaints = db.query(Complaint).filter(
        Complaint.link_id.in_(link_ids),
        Complaint.status.in_([ComplaintStatus.OPEN, ComplaintStatus.IN_PROGRESS, ComplaintStatus.ESCALATED])
    ).all()
    
    return complaints
