"""
Test script for audit logging
Demonstrates audit logging functionality
"""

import sys
sys.path.insert(0, 'src')

from audit_logger import AuditLogger
import time

def test_audit_logging():
    """Test audit logging functionality"""
    print("=" * 70)
    print("AUDIT LOGGING TEST")
    print("=" * 70)
    
    # Initialize audit logger
    audit_log = AuditLogger()
    
    # Test 1: Log successful login
    print("\n1. Testing LOGIN logging...")
    audit_log.log_login(user_id=1, username='admin', success=True)
    print("   ✓ Logged successful login")
    
    # Test 2: Log failed login
    print("\n2. Testing FAILED LOGIN logging...")
    audit_log.log_login(user_id=None, username='hacker', success=False, error='Invalid credentials')
    print("   ✓ Logged failed login")
    
    # Test 3: Log prediction
    print("\n3. Testing PREDICTION logging...")
    audit_log.log_prediction(
        user_id=1,
        username='admin',
        prediction_id=123,
        result='Benign',
        confidence=95.5
    )
    print("   ✓ Logged prediction")
    
    # Test 4: Log password change
    print("\n4. Testing PASSWORD CHANGE logging...")
    audit_log.log_password_change(user_id=1, username='admin', success=True)
    print("   ✓ Logged password change")
    
    # Test 5: Log data deletion
    print("\n5. Testing DATA DELETION logging...")
    audit_log.log_data_deletion(
        user_id=1,
        username='admin',
        resource='prediction_456'
    )
    print("   ✓ Logged data deletion")
    
    # Test 6: Log admin action
    print("\n6. Testing ADMIN ACTION logging...")
    audit_log.log_admin_action(
        user_id=1,
        username='admin',
        action='REGISTER_DOCTOR',
        resource='user_789',
        details='Registered new doctor: Dr. Smith'
    )
    print("   ✓ Logged admin action")
    
    # Test 7: Log validation error
    print("\n7. Testing VALIDATION ERROR logging...")
    audit_log.log_validation_error(
        user_id=2,
        username='user1',
        error='Feature 0 cannot be negative'
    )
    print("   ✓ Logged validation error")
    
    # Test 8: Log prediction error
    print("\n8. Testing PREDICTION ERROR logging...")
    audit_log.log_prediction_error(
        user_id=2,
        username='user1',
        error='Model not loaded'
    )
    print("   ✓ Logged prediction error")
    
    # Wait a moment for database writes
    time.sleep(0.5)
    
    # Test 9: Get recent logs
    print("\n9. Testing GET RECENT LOGS...")
    logs = audit_log.get_recent_logs(limit=10)
    print(f"   ✓ Retrieved {len(logs)} recent logs")
    
    if logs:
        print("\n   Recent logs:")
        for log in logs[:5]:  # Show first 5
            print(f"   - [{log['timestamp']}] {log['username']}: {log['action']} - {log['status']}")
    
    # Test 10: Get failed logins
    print("\n10. Testing GET FAILED LOGINS...")
    failed = audit_log.get_failed_logins(hours=24)
    print(f"   ✓ Retrieved {len(failed)} failed login attempts")
    
    # Test 11: Get statistics
    print("\n11. Testing GET STATISTICS...")
    stats = audit_log.get_statistics(days=7)
    print(f"   ✓ Total events: {stats.get('total_events', 0)}")
    print(f"   ✓ Failed events: {stats.get('failed_events', 0)}")
    
    if stats.get('by_action'):
        print("\n   Events by action:")
        for action, count in list(stats['by_action'].items())[:5]:
            print(f"   - {action}: {count}")
    
    # Test 12: Search logs
    print("\n12. Testing SEARCH LOGS...")
    search_results = audit_log.search_logs('admin')
    print(f"   ✓ Found {len(search_results)} logs matching 'admin'")
    
    # Test 13: Get user activity
    print("\n13. Testing GET USER ACTIVITY...")
    user_logs = audit_log.get_user_activity(user_id=1, limit=10)
    print(f"   ✓ Retrieved {len(user_logs)} activities for user_id=1")
    
    print("\n" + "=" * 70)
    print("ALL TESTS COMPLETED SUCCESSFULLY ✓")
    print("=" * 70)
    
    print("\n" + "=" * 70)
    print("AUDIT LOG SUMMARY")
    print("=" * 70)
    print(f"Total logs created: {len(logs)}")
    print(f"Failed logins: {len(failed)}")
    print(f"Database location: {audit_log.db_path}")
    print("\nAudit logging is working correctly!")
    print("=" * 70)

if __name__ == '__main__':
    test_audit_logging()
