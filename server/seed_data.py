"""
Скрипт для наполнения БД тестовыми данными
Создает несколько suppliers (с owner, manager, sales) и consumers
с заказами, сообщениями и жалобами
"""

from database import SessionLocal, init_db
from models import (
    User, Supplier, Consumer, Link, Product, Order, OrderItem,
    Message, Complaint, UserRole, LinkStatus, OrderStatus, 
    ComplaintStatus, MessageType
)
from utils.security import get_password_hash
from datetime import datetime, timedelta

def seed_database():
    """Заполнить БД тестовыми данными"""
    
    # Инициализируем БД
    init_db()
    
    db = SessionLocal()
    
    try:
        print("🌱 Starting database seeding...")
        
        # Проверяем, есть ли уже данные
        existing_users = db.query(User).count()
        if existing_users > 0:
            print("⚠️  Database already contains data. Clearing...")
            # Очищаем существующие данные
            db.query(Complaint).delete()
            db.query(Message).delete()
            db.query(OrderItem).delete()
            db.query(Order).delete()
            db.query(Product).delete()
            db.query(Link).delete()
            db.query(Consumer).delete()
            db.query(Supplier).delete()
            db.query(User).delete()
            db.commit()
        
        # Пароль для всех тестовых пользователей
        test_password = get_password_hash("password123")
        
        # ========== SUPPLIER 1: Fresh Products Co. ==========
        print("\n📦 Creating Supplier 1: Fresh Products Co...")
        
        # Owner
        owner1 = User(
            email="owner1@freshproducts.kz",
            phone="+77001234567",
            full_name="Алексей Иванов",
            hashed_password=test_password,
            role=UserRole.OWNER,
            is_active=True
        )
        db.add(owner1)
        db.flush()
        
        supplier1 = Supplier(
            user_id=owner1.id,
            company_name="Fresh Products Co.",
            company_address="г. Алматы, ул. Абая 150",
            tax_id="KZ123456789012",
            description="Поставщик свежих продуктов и овощей"
        )
        db.add(supplier1)
        db.flush()
        
        # Manager
        manager1 = User(
            email="manager1@freshproducts.kz",
            phone="+77001234568",
            full_name="Марина Петрова",
            hashed_password=test_password,
            role=UserRole.MANAGER,
            is_active=True
        )
        db.add(manager1)
        db.flush()
        
        supplier1_manager = Supplier(
            user_id=manager1.id,
            company_name=supplier1.company_name,
            company_address=supplier1.company_address,
            tax_id=supplier1.tax_id,
            description=supplier1.description
        )
        db.add(supplier1_manager)
        
        # Sales Representative
        sales1 = User(
            email="sales1@freshproducts.kz",
            phone="+77001234569",
            full_name="Дмитрий Сидоров",
            hashed_password=test_password,
            role=UserRole.SALES,
            is_active=True
        )
        db.add(sales1)
        db.flush()
        
        supplier1_sales = Supplier(
            user_id=sales1.id,
            company_name=supplier1.company_name,
            company_address=supplier1.company_address,
            tax_id=supplier1.tax_id,
            description=supplier1.description
        )
        db.add(supplier1_sales)
        db.flush()
        
        # Products for Supplier 1
        products1 = [
            Product(
                supplier_id=supplier1.id,
                name="Помидоры",
                description="Свежие красные помидоры",
                category="Овощи",
                unit="кг",
                price=500.00,
                stock_quantity=100,
                is_available=True
            ),
            Product(
                supplier_id=supplier1.id,
                name="Огурцы",
                description="Свежие огурцы",
                category="Овощи",
                unit="кг",
                price=400.00,
                stock_quantity=80,
                is_available=True
            ),
            Product(
                supplier_id=supplier1.id,
                name="Картофель",
                description="Молодой картофель",
                category="Овощи",
                unit="кг",
                price=200.00,
                stock_quantity=200,
                is_available=True
            ),
            Product(
                supplier_id=supplier1.id,
                name="Лук",
                description="Репчатый лук",
                category="Овощи",
                unit="кг",
                price=150.00,
                stock_quantity=150,
                is_available=True
            ),
        ]
        for product in products1:
            db.add(product)
        
        # ========== SUPPLIER 2: Meat & Dairy Ltd. ==========
        print("📦 Creating Supplier 2: Meat & Dairy Ltd...")
        
        # Owner
        owner2 = User(
            email="owner2@meatdairy.kz",
            phone="+77002345678",
            full_name="Сергей Козлов",
            hashed_password=test_password,
            role=UserRole.OWNER,
            is_active=True
        )
        db.add(owner2)
        db.flush()
        
        supplier2 = Supplier(
            user_id=owner2.id,
            company_name="Meat & Dairy Ltd.",
            company_address="г. Нур-Султан, пр. Кабанбай батыра 42",
            tax_id="KZ987654321098",
            description="Мясо-молочная продукция высшего качества"
        )
        db.add(supplier2)
        db.flush()
        
        # Manager
        manager2 = User(
            email="manager2@meatdairy.kz",
            phone="+77002345679",
            full_name="Ольга Смирнова",
            hashed_password=test_password,
            role=UserRole.MANAGER,
            is_active=True
        )
        db.add(manager2)
        db.flush()
        
        supplier2_manager = Supplier(
            user_id=manager2.id,
            company_name=supplier2.company_name,
            company_address=supplier2.company_address,
            tax_id=supplier2.tax_id,
            description=supplier2.description
        )
        db.add(supplier2_manager)
        
        # Sales Representative
        sales2 = User(
            email="sales2@meatdairy.kz",
            phone="+77002345680",
            full_name="Анна Васильева",
            hashed_password=test_password,
            role=UserRole.SALES,
            is_active=True
        )
        db.add(sales2)
        db.flush()
        
        supplier2_sales = Supplier(
            user_id=sales2.id,
            company_name=supplier2.company_name,
            company_address=supplier2.company_address,
            tax_id=supplier2.tax_id,
            description=supplier2.description
        )
        db.add(supplier2_sales)
        db.flush()
        
        # Products for Supplier 2
        products2 = [
            Product(
                supplier_id=supplier2.id,
                name="Говядина",
                description="Свежая говядина премиум",
                category="Мясо",
                unit="кг",
                price=3500.00,
                stock_quantity=50,
                is_available=True
            ),
            Product(
                supplier_id=supplier2.id,
                name="Курица",
                description="Охлажденная курица",
                category="Мясо",
                unit="кг",
                price=1200.00,
                stock_quantity=100,
                is_available=True
            ),
            Product(
                supplier_id=supplier2.id,
                name="Молоко",
                description="Свежее коровье молоко",
                category="Молочные продукты",
                unit="л",
                price=350.00,
                stock_quantity=200,
                is_available=True
            ),
            Product(
                supplier_id=supplier2.id,
                name="Сыр",
                description="Твердый сыр",
                category="Молочные продукты",
                unit="кг",
                price=2500.00,
                stock_quantity=30,
                is_available=True
            ),
        ]
        for product in products2:
            db.add(product)
        
        db.flush()
        
        # ========== CONSUMERS ==========
        print("\n🍽️  Creating Consumers...")
        
        # Consumer 1: Restaurant
        consumer1_user = User(
            email="restaurant1@example.kz",
            phone="+77003456789",
            full_name="Айгуль Нурланова",
            hashed_password=test_password,
            role=UserRole.CONSUMER,
            is_active=True
        )
        db.add(consumer1_user)
        db.flush()
        
        consumer1 = Consumer(
            user_id=consumer1_user.id,
            business_name="Ресторан 'Султан'",
            business_type="restaurant",
            address="г. Алматы, ул. Достык 234"
        )
        db.add(consumer1)
        
        # Consumer 2: Hotel
        consumer2_user = User(
            email="hotel1@example.kz",
            phone="+77003456790",
            full_name="Ерлан Бекмуратов",
            hashed_password=test_password,
            role=UserRole.CONSUMER,
            is_active=True
        )
        db.add(consumer2_user)
        db.flush()
        
        consumer2 = Consumer(
            user_id=consumer2_user.id,
            business_name="Отель 'Рахат'",
            business_type="hotel",
            address="г. Алматы, пр. Назарбаева 75"
        )
        db.add(consumer2)
        
        # Consumer 3: Cafe
        consumer3_user = User(
            email="cafe1@example.kz",
            phone="+77003456791",
            full_name="Дина Касымова",
            hashed_password=test_password,
            role=UserRole.CONSUMER,
            is_active=True
        )
        db.add(consumer3_user)
        db.flush()
        
        consumer3 = Consumer(
            user_id=consumer3_user.id,
            business_name="Кафе 'Арман'",
            business_type="cafe",
            address="г. Нур-Султан, ул. Жібек жолы 12"
        )
        db.add(consumer3)
        db.flush()
        
        # ========== LINKS ==========
        print("\n🔗 Creating Links...")
        
        # Consumer 1 -> Supplier 1 (ACCEPTED)
        link1 = Link(
            consumer_id=consumer1.id,
            supplier_id=supplier1.id,
            status=LinkStatus.ACCEPTED,
            requested_at=datetime.utcnow() - timedelta(days=10),
            responded_at=datetime.utcnow() - timedelta(days=9),
            notes="Одобрено"
        )
        db.add(link1)
        
        # Consumer 1 -> Supplier 2 (ACCEPTED)
        link2 = Link(
            consumer_id=consumer1.id,
            supplier_id=supplier2.id,
            status=LinkStatus.ACCEPTED,
            requested_at=datetime.utcnow() - timedelta(days=8),
            responded_at=datetime.utcnow() - timedelta(days=7),
            notes="Одобрено"
        )
        db.add(link2)
        
        # Consumer 2 -> Supplier 1 (PENDING)
        link3 = Link(
            consumer_id=consumer2.id,
            supplier_id=supplier1.id,
            status=LinkStatus.PENDING,
            requested_at=datetime.utcnow() - timedelta(days=2),
            notes="Ожидает одобрения"
        )
        db.add(link3)
        
        # Consumer 2 -> Supplier 2 (ACCEPTED)
        link4 = Link(
            consumer_id=consumer2.id,
            supplier_id=supplier2.id,
            status=LinkStatus.ACCEPTED,
            requested_at=datetime.utcnow() - timedelta(days=5),
            responded_at=datetime.utcnow() - timedelta(days=4),
            notes="Одобрено"
        )
        db.add(link4)
        
        # Consumer 3 -> Supplier 1 (ACCEPTED)
        link5 = Link(
            consumer_id=consumer3.id,
            supplier_id=supplier1.id,
            status=LinkStatus.ACCEPTED,
            requested_at=datetime.utcnow() - timedelta(days=6),
            responded_at=datetime.utcnow() - timedelta(days=5),
            notes="Одобрено"
        )
        db.add(link5)
        
        # Consumer 3 -> Supplier 2 (REJECTED)
        link6 = Link(
            consumer_id=consumer3.id,
            supplier_id=supplier2.id,
            status=LinkStatus.REJECTED,
            requested_at=datetime.utcnow() - timedelta(days=3),
            responded_at=datetime.utcnow() - timedelta(days=2),
            notes="Не подходит по условиям"
        )
        db.add(link6)
        
        db.flush()
        
        # ========== ORDERS ==========
        print("\n📋 Creating Orders...")
        
        # Order 1: Consumer 1 -> Supplier 1 (DELIVERED - для жалобы)
        order1 = Order(
            consumer_id=consumer1.id,
            supplier_id=supplier1.id,
            status=OrderStatus.DELIVERED,
            total_amount=3500.00,
            notes="Срочная доставка",
            created_at=datetime.utcnow() - timedelta(days=5)
        )
        db.add(order1)
        db.flush()
        
        order1_items = [
            OrderItem(
                order_id=order1.id,
                product_id=products1[0].id,  # Помидоры
                quantity=5,
                unit_price=500.00,
                total_price=2500.00
            ),
            OrderItem(
                order_id=order1.id,
                product_id=products1[1].id,  # Огурцы
                quantity=2,
                unit_price=400.00,
                total_price=800.00
            ),
            OrderItem(
                order_id=order1.id,
                product_id=products1[3].id,  # Лук
                quantity=1,
                unit_price=150.00,
                total_price=150.00
            ),
        ]
        for item in order1_items:
            db.add(item)
        
        # Order 2: Consumer 1 -> Supplier 2 (ACCEPTED)
        order2 = Order(
            consumer_id=consumer1.id,
            supplier_id=supplier2.id,
            status=OrderStatus.ACCEPTED,
            total_amount=8700.00,
            created_at=datetime.utcnow() - timedelta(days=2)
        )
        db.add(order2)
        db.flush()
        
        order2_items = [
            OrderItem(
                order_id=order2.id,
                product_id=products2[0].id,  # Говядина
                quantity=2,
                unit_price=3500.00,
                total_price=7000.00
            ),
            OrderItem(
                order_id=order2.id,
                product_id=products2[2].id,  # Молоко
                quantity=5,
                unit_price=350.00,
                total_price=1750.00
            ),
        ]
        for item in order2_items:
            db.add(item)
        
        # Order 3: Consumer 2 -> Supplier 2 (PENDING)
        order3 = Order(
            consumer_id=consumer2.id,
            supplier_id=supplier2.id,
            status=OrderStatus.PENDING,
            total_amount=6200.00,
            created_at=datetime.utcnow() - timedelta(hours=5)
        )
        db.add(order3)
        db.flush()
        
        order3_items = [
            OrderItem(
                order_id=order3.id,
                product_id=products2[1].id,  # Курица
                quantity=5,
                unit_price=1200.00,
                total_price=6000.00
            ),
        ]
        for item in order3_items:
            db.add(item)
        
        # Order 4: Consumer 3 -> Supplier 1 (DELIVERED - для жалобы)
        order4 = Order(
            consumer_id=consumer3.id,
            supplier_id=supplier1.id,
            status=OrderStatus.DELIVERED,
            total_amount=2000.00,
            created_at=datetime.utcnow() - timedelta(days=3)
        )
        db.add(order4)
        db.flush()
        
        order4_items = [
            OrderItem(
                order_id=order4.id,
                product_id=products1[2].id,  # Картофель
                quantity=10,
                unit_price=200.00,
                total_price=2000.00
            ),
        ]
        for item in order4_items:
            db.add(item)
        
        db.flush()
        
        # ========== MESSAGES ==========
        print("\n💬 Creating Messages...")
        
        # Messages for Link 1 (Consumer 1 <-> Supplier 1)
        msg1 = Message(
            link_id=link1.id,
            sender_id=consumer1_user.id,
            message_type=MessageType.TEXT,
            content="Здравствуйте! Когда можно ожидать следующую поставку?",
            created_at=datetime.utcnow() - timedelta(days=4),
            is_read=True
        )
        db.add(msg1)
        
        msg2 = Message(
            link_id=link1.id,
            sender_id=sales1.id,
            message_type=MessageType.TEXT,
            content="Добрый день! Следующая поставка планируется на завтра утром.",
            created_at=datetime.utcnow() - timedelta(days=4, hours=-2),
            is_read=True
        )
        db.add(msg2)
        
        msg3 = Message(
            link_id=link1.id,
            sender_id=consumer1_user.id,
            message_type=MessageType.TEXT,
            content="Отлично, спасибо!",
            created_at=datetime.utcnow() - timedelta(days=4, hours=-3),
            is_read=True
        )
        db.add(msg3)
        
        # Messages for Link 2 (Consumer 1 <-> Supplier 2)
        msg4 = Message(
            link_id=link2.id,
            sender_id=consumer1_user.id,
            message_type=MessageType.TEXT,
            content="Добрый день! Есть ли в наличии свежая говядина?",
            created_at=datetime.utcnow() - timedelta(days=1),
            is_read=False
        )
        db.add(msg4)
        
        db.flush()
        
        # ========== COMPLAINTS ==========
        print("\n⚠️  Creating Complaints...")
        
        # Complaint 1: Consumer 1 -> Order 1 (DELIVERED) - IN_PROGRESS у Sales
        complaint1 = Complaint(
            order_id=order1.id,
            link_id=link1.id,
            created_by_id=consumer1_user.id,
            assigned_to_id=sales1.id,
            title="Плохое качество помидоров",
            description="Половина помидоров в заказе оказались испорченными. Требуется замена.",
            status=ComplaintStatus.IN_PROGRESS,
            priority="high",
            created_at=datetime.utcnow() - timedelta(days=3)
        )
        db.add(complaint1)
        
        # Complaint 2: Consumer 3 -> Order 4 (DELIVERED) - ESCALATED к Manager
        complaint2 = Complaint(
            order_id=order4.id,
            link_id=link5.id,
            created_by_id=consumer3_user.id,
            assigned_to_id=manager1.id,  # Эскалировано к Manager
            title="Неполная поставка",
            description="Заказывали 10 кг картофеля, привезли только 8 кг. Требуется доставка недостающего количества.",
            status=ComplaintStatus.ESCALATED,
            priority="normal",
            created_at=datetime.utcnow() - timedelta(days=2)
        )
        db.add(complaint2)
        
        db.commit()
        
        print("\n✅ Database seeding completed successfully!")
        print("\n📊 Summary:")
        print(f"   - Suppliers: 2")
        print(f"   - Owners: 2")
        print(f"   - Managers: 2")
        print(f"   - Sales Representatives: 2")
        print(f"   - Consumers: 3")
        print(f"   - Products: {len(products1) + len(products2)}")
        print(f"   - Links: 6")
        print(f"   - Orders: 4")
        print(f"   - Messages: 4")
        print(f"   - Complaints: 2")
        
        print("\n👤 Test Users:")
        print("\n   Supplier 1 - Fresh Products Co.:")
        print("   - Owner:    owner1@freshproducts.kz / password123")
        print("   - Manager:  manager1@freshproducts.kz / password123")
        print("   - Sales:    sales1@freshproducts.kz / password123")
        
        print("\n   Supplier 2 - Meat & Dairy Ltd.:")
        print("   - Owner:    owner2@meatdairy.kz / password123")
        print("   - Manager:  manager2@meatdairy.kz / password123")
        print("   - Sales:    sales2@meatdairy.kz / password123")
        
        print("\n   Consumers:")
        print("   - Restaurant: restaurant1@example.kz / password123")
        print("   - Hotel:      hotel1@example.kz / password123")
        print("   - Cafe:       cafe1@example.kz / password123")
        
    except Exception as e:
        print(f"\n❌ Error during seeding: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
