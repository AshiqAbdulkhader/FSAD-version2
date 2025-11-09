from flask import Blueprint, jsonify
from config.database import query_db
from middleware.auth import token_required, role_required, get_current_user

bp = Blueprint('dashboard', __name__)

@bp.route('/stats', methods=['GET'])
@role_required('admin')
def get_stats():
    """Get dashboard statistics (admin only)"""
    try:
        # Total equipment count
        total_equipment = query_db(
            'SELECT COUNT(*) FROM equipment',
            fetch_one=True
        )
        
        # Total users count
        total_users = query_db(
            'SELECT COUNT(*) FROM users',
            fetch_one=True
        )
        
        # Pending requests count
        pending_requests = query_db(
            "SELECT COUNT(*) FROM borrowing_requests WHERE status = 'pending'",
            fetch_one=True
        )
        
        # Active borrowings count
        active_borrowings = query_db(
            "SELECT COUNT(*) FROM borrowing_requests WHERE status = 'approved' AND CURRENT_DATE BETWEEN start_date AND end_date",
            fetch_one=True
        )
        
        # Equipment by category
        equipment_by_category = query_db(
            'SELECT category, COUNT(*) FROM equipment GROUP BY category',
            fetch_all=True
        )
        
        # Requests by status
        requests_by_status = query_db(
            'SELECT status, COUNT(*) FROM borrowing_requests GROUP BY status',
            fetch_all=True
        )
        
        return jsonify({
            'total_equipment': total_equipment[0] if total_equipment else 0,
            'total_users': total_users[0] if total_users else 0,
            'pending_requests': pending_requests[0] if pending_requests else 0,
            'active_borrowings': active_borrowings[0] if active_borrowings else 0,
            'equipment_by_category': {cat[0]: cat[1] for cat in equipment_by_category},
            'requests_by_status': {status[0]: status[1] for status in requests_by_status}
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

