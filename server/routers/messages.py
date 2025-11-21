from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.responses import Response
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models import User, Message, Link, LinkStatus, MessageType, UserRole, Supplier
from schemas import MessageCreate, MessageResponse
from utils.security import get_current_active_user
from utils.permissions import get_consumer_id, get_supplier_id

router = APIRouter(prefix="/api/messages", tags=["Messages"])

def check_link_access(user: User, link_id: int, db: Session):
    """Проверка доступа к чату через link"""
    link = db.query(Link).filter(Link.id == link_id).first()
    
    if not link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Link not found"
        )
    
    # Проверяем что связь принята
    if link.status != LinkStatus.ACCEPTED:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Link must be accepted to send messages"
        )
    
    # Проверяем доступ пользователя
    if user.role == UserRole.CONSUMER:
        consumer_id = get_consumer_id(user, db)
        if link.consumer_id != consumer_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    else:
        # Получаем company_name текущего пользователя
        supplier_record = db.query(Supplier).filter(Supplier.user_id == user.id).first()
        if not supplier_record:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        
        company_name = supplier_record.company_name
        
        # Находим все записи Supplier с таким же company_name
        supplier_ids = db.query(Supplier.id).filter(Supplier.company_name == company_name).all()
        supplier_ids = [sid[0] for sid in supplier_ids]
        
        # Проверяем что link принадлежит нашей компании
        if link.supplier_id not in supplier_ids:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
    return link

@router.post("/", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
def send_message(
    message_data: MessageCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Отправить текстовое сообщение"""
    check_link_access(current_user, message_data.link_id, db)
    
    message = Message(
        link_id=message_data.link_id,
        sender_id=current_user.id,
        message_type=message_data.message_type,
        content=message_data.content
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    
    # Преобразуем в response
    msg_dict = MessageResponse.from_orm(message)
    msg_dict.has_file = False
    
    return msg_dict

@router.post("/upload", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
def send_file_message(
    link_id: int,
    message_type: MessageType,
    file: UploadFile = File(...),
    content: Optional[str] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Отправить сообщение с файлом (изображение, документ, аудио)"""
    check_link_access(current_user, link_id, db)
    
    # Читаем файл
    file_data = file.file.read()
    
    message = Message(
        link_id=link_id,
        sender_id=current_user.id,
        message_type=message_type,
        content=content,
        file_data=file_data,
        file_name=file.filename,
        file_mime_type=file.content_type
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    
    msg_dict = MessageResponse.from_orm(message)
    msg_dict.has_file = True
    
    return msg_dict

@router.get("/link/{link_id}", response_model=List[MessageResponse])
def get_messages(
    link_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Получить все сообщения для link"""
    check_link_access(current_user, link_id, db)
    
    messages = db.query(Message).filter(
        Message.link_id == link_id
    ).order_by(Message.created_at.asc()).offset(skip).limit(limit).all()
    
    result = []
    for msg in messages:
        msg_dict = MessageResponse.from_orm(msg)
        msg_dict.has_file = msg.file_data is not None
        result.append(msg_dict)
    
    return result

@router.get("/{message_id}/file")
def get_message_file(
    message_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Получить файл из сообщения"""
    message = db.query(Message).filter(Message.id == message_id).first()
    
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found"
        )
    
    # Проверяем доступ через link
    check_link_access(current_user, message.link_id, db)
    
    if not message.file_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )
    
    return Response(
        content=message.file_data,
        media_type=message.file_mime_type or "application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename={message.file_name}"}
    )

@router.put("/{message_id}/read")
def mark_as_read(
    message_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Отметить сообщение как прочитанное"""
    message = db.query(Message).filter(Message.id == message_id).first()
    
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found"
        )
    
    check_link_access(current_user, message.link_id, db)
    
    message.is_read = True
    db.commit()
    
    return {"message": "Marked as read"}

@router.get("/unread/count")
def get_unread_count(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Получить количество непрочитанных сообщений"""
    
    # Получаем все links пользователя
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
            return {"unread_count": 0}
        
        company_name = supplier_record.company_name
        
        # Находим все записи Supplier с таким же company_name
        supplier_ids = db.query(Supplier.id).filter(Supplier.company_name == company_name).all()
        supplier_ids = [sid[0] for sid in supplier_ids]
        
        # Получаем links для всех supplier_id с этим company_name
        links = db.query(Link).filter(
            Link.supplier_id.in_(supplier_ids),
            Link.status == LinkStatus.ACCEPTED
        ).all()
    
    link_ids = [link.id for link in links]
    
    # Считаем непрочитанные сообщения (не от текущего пользователя)
    unread_count = db.query(Message).filter(
        Message.link_id.in_(link_ids),
        Message.sender_id != current_user.id,
        Message.is_read == False
    ).count()
    
    return {"unread_count": unread_count}
