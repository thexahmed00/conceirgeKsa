"""Quick script to create test notifications."""

from src.infrastructure.persistence.database import SessionLocal
from src.infrastructure.persistence.repositories.notification_repository import PostgreSQLNotificationRepository
from src.application.notification.services.notification_service import NotificationService

def create_test_notifications():
    """Create some test notifications for user ID 9."""
    db = SessionLocal()
    try:
        notification_service = NotificationService(db)
        
        # Create a few test notifications for user_id=9
        print("Creating test notifications for user_id=9...")
        
        # 1. Welcome notification
        notification_service.notify_general(
            user_id=9,
            title="Welcome to AJLA Concierge!",
            message="Thank you for joining our premium lifestyle concierge service. We're here to help you with all your needs."
        )
        print("✓ Created welcome notification")
        
        # 2. Booking confirmed notification
        notification_service.notify_booking_confirmed(
            user_id=9,
            booking_id=1,
            booking_details="Luxury Car Rental - Mercedes S-Class"
        )
        print("✓ Created booking confirmation notification")
        
        # 3. Message received notification
        notification_service.notify_message_received(
            user_id=9,
            conversation_id=1,
            sender_name="Support Team"
        )
        print("✓ Created message notification")
        
        # 4. Request updated notification
        notification_service.notify_request_updated(
            user_id=9,
            request_id=1,
            status="in_progress"
        )
        print("✓ Created request update notification")
        
        print("\n✅ Successfully created 4 test notifications!")
        print("Now try: GET /api/v1/notifications")
        
    except Exception as e:
        print(f"❌ Error creating notifications: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_test_notifications()
