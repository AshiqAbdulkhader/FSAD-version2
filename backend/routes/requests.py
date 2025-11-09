from flask import Blueprint, request, jsonify
from datetime import datetime
from config.database import query_db
from middleware.auth import token_required, role_required, get_current_user

bp = Blueprint('requests', __name__)

@bp.route('', methods=['GET'])
@token_required
def get_requests():
    """Get borrowing requests (filtered by user role)"""
    try:
        user = get_current_user()
        status = request.args.get('status')
        
        if user['role'] == 'admin' or user['role'] == 'staff':
            # Admin/Staff can see all requests
            query = '''SELECT br.id, br.user_id, u.name as user_name, u.email as user_email,
                      br.equipment_id, e.name as equipment_name, br.request_date,
                      br.start_date, br.end_date, br.status, br.approved_by, br.approval_date, br.return_date
                      FROM borrowing_requests br
                      JOIN users u ON br.user_id = u.id
                      JOIN equipment e ON br.equipment_id = e.id
                      WHERE 1=1'''
            params = []
        else:
            # Students can only see their own requests
            query = '''SELECT br.id, br.user_id, u.name as user_name, u.email as user_email,
                      br.equipment_id, e.name as equipment_name, br.request_date,
                      br.start_date, br.end_date, br.status, br.approved_by, br.approval_date, br.return_date
                      FROM borrowing_requests br
                      JOIN users u ON br.user_id = u.id
                      JOIN equipment e ON br.equipment_id = e.id
                      WHERE br.user_id = %s'''
            params = [user['id']]
        
        if status:
            query += ' AND br.status = %s'
            params.append(status)
        
        query += ' ORDER BY br.request_date DESC'
        
        requests = query_db(query, tuple(params), fetch_all=True)
        
        result = []
        for req in requests:
            result.append({
                'id': req[0],
                'user_id': req[1],
                'user_name': req[2],
                'user_email': req[3],
                'equipment_id': req[4],
                'equipment_name': req[5],
                'request_date': req[6].isoformat() if req[6] else None,
                'start_date': req[7].isoformat() if req[7] else None,
                'end_date': req[8].isoformat() if req[8] else None,
                'status': req[9],
                'approved_by': req[10],
                'approval_date': req[11].isoformat() if req[11] else None,
                'return_date': req[12].isoformat() if req[12] else None
            })
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:request_id>', methods=['GET'])
@token_required
def get_request_by_id(request_id):
    """Get single request by ID"""
    try:
        user = get_current_user()
        
        request_data = query_db(
            '''SELECT br.id, br.user_id, u.name as user_name, u.email as user_email,
               br.equipment_id, e.name as equipment_name, br.request_date,
               br.start_date, br.end_date, br.status, br.approved_by, br.approval_date, br.return_date
               FROM borrowing_requests br
               JOIN users u ON br.user_id = u.id
               JOIN equipment e ON br.equipment_id = e.id
               WHERE br.id = %s''',
            (request_id,),
            fetch_one=True
        )
        
        if not request_data:
            return jsonify({'error': 'Request not found'}), 404
        
        # Check if user has permission to view this request
        if user['role'] not in ['admin', 'staff'] and request_data[1] != user['id']:
            return jsonify({'error': 'Unauthorized'}), 403
        
        return jsonify({
            'id': request_data[0],
            'user_id': request_data[1],
            'user_name': request_data[2],
            'user_email': request_data[3],
            'equipment_id': request_data[4],
            'equipment_name': request_data[5],
            'request_date': request_data[6].isoformat() if request_data[6] else None,
            'start_date': request_data[7].isoformat() if request_data[7] else None,
            'end_date': request_data[8].isoformat() if request_data[8] else None,
            'status': request_data[9],
            'approved_by': request_data[10],
            'approval_date': request_data[11].isoformat() if request_data[11] else None,
            'return_date': request_data[12].isoformat() if request_data[12] else None
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('', methods=['POST'])
@token_required
def create_request():
    """Create new borrowing request"""
    try:
        user = get_current_user()
        data = request.get_json()
        
        equipment_id = data.get('equipment_id')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        
        if not all([equipment_id, start_date, end_date]):
            return jsonify({'error': 'Equipment ID, start date, and end date are required'}), 400
        
        # Validate dates
        try:
            start = datetime.strptime(start_date, '%Y-%m-%d').date()
            end = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
        
        if start > end:
            return jsonify({'error': 'Start date must be before or equal to end date'}), 400
        
        if start < datetime.now().date():
            return jsonify({'error': 'Start date cannot be in the past'}), 400
        
        # Check if equipment exists
        equipment = query_db(
            'SELECT id, quantity FROM equipment WHERE id = %s',
            (equipment_id,),
            fetch_one=True
        )
        
        if not equipment:
            return jsonify({'error': 'Equipment not found'}), 404
        
        # Check for overlapping bookings
        overlapping = query_db(
            '''SELECT COUNT(*) FROM borrowing_requests
               WHERE equipment_id = %s AND status = 'approved'
               AND ((start_date <= %s AND end_date >= %s)
               OR (start_date <= %s AND end_date >= %s)
               OR (start_date >= %s AND end_date <= %s))''',
            (equipment_id, start, start, end, end, start, end),
            fetch_one=True
        )
        
        if overlapping and overlapping[0] > 0:
            # Check if there's available quantity
            active_count = query_db(
                '''SELECT COUNT(*) FROM borrowing_requests
                   WHERE equipment_id = %s AND status = 'approved'
                   AND ((start_date <= %s AND end_date >= %s)
                   OR (start_date <= %s AND end_date >= %s)
                   OR (start_date >= %s AND end_date <= %s))''',
                (equipment_id, start, start, end, end, start, end),
                fetch_one=True
            )
            
            if active_count and active_count[0] >= equipment[1]:
                return jsonify({'error': 'Equipment not available for the selected dates'}), 400
        
        # Create request
        query_db(
            'INSERT INTO borrowing_requests (user_id, equipment_id, start_date, end_date) VALUES (%s, %s, %s, %s)',
            (user['id'], equipment_id, start_date, end_date)
        )
        
        return jsonify({'message': 'Request created successfully'}), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:request_id>/approve', methods=['PUT'])
@role_required('admin', 'staff')
def approve_request(request_id):
    """Approve a borrowing request (staff/admin only)"""
    try:
        user = get_current_user()
        
        # Get request
        request_data = query_db(
            'SELECT id, equipment_id, start_date, end_date, status FROM borrowing_requests WHERE id = %s',
            (request_id,),
            fetch_one=True
        )
        
        if not request_data:
            return jsonify({'error': 'Request not found'}), 404
        
        if request_data[4] != 'pending':
            return jsonify({'error': 'Request is not pending'}), 400
        
        # Check for overlapping bookings
        equipment = query_db(
            'SELECT quantity FROM equipment WHERE id = %s',
            (request_data[1],),
            fetch_one=True
        )
        
        if equipment:
            overlapping = query_db(
                '''SELECT COUNT(*) FROM borrowing_requests
                   WHERE equipment_id = %s AND status = 'approved' AND id != %s
                   AND ((start_date <= %s AND end_date >= %s)
                   OR (start_date <= %s AND end_date >= %s)
                   OR (start_date >= %s AND end_date <= %s))''',
                (request_data[1], request_id, request_data[2], request_data[2],
                 request_data[3], request_data[3], request_data[2], request_data[3]),
                fetch_one=True
            )
            
            if overlapping and overlapping[0] >= equipment[0]:
                return jsonify({'error': 'Cannot approve: Equipment not available for the selected dates'}), 400
        
        # Approve request
        query_db(
            '''UPDATE borrowing_requests 
               SET status = 'approved', approved_by = %s, approval_date = CURRENT_TIMESTAMP
               WHERE id = %s''',
            (user['id'], request_id)
        )
        
        return jsonify({'message': 'Request approved successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:request_id>/reject', methods=['PUT'])
@role_required('admin', 'staff')
def reject_request(request_id):
    """Reject a borrowing request (staff/admin only)"""
    try:
        user = get_current_user()
        
        # Get request
        request_data = query_db(
            'SELECT id, status FROM borrowing_requests WHERE id = %s',
            (request_id,),
            fetch_one=True
        )
        
        if not request_data:
            return jsonify({'error': 'Request not found'}), 404
        
        if request_data[1] != 'pending':
            return jsonify({'error': 'Only pending requests can be rejected'}), 400
        
        # Reject request
        query_db(
            '''UPDATE borrowing_requests 
               SET status = 'rejected', approved_by = %s, approval_date = CURRENT_TIMESTAMP
               WHERE id = %s''',
            (user['id'], request_id)
        )
        
        return jsonify({'message': 'Request rejected successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:request_id>/return', methods=['PUT'])
@role_required('admin', 'staff')
def mark_returned(request_id):
    """Mark equipment as returned (staff/admin only)"""
    try:
        # Get request
        request_data = query_db(
            'SELECT id, status FROM borrowing_requests WHERE id = %s',
            (request_id,),
            fetch_one=True
        )
        
        if not request_data:
            return jsonify({'error': 'Request not found'}), 404
        
        if request_data[1] != 'approved':
            return jsonify({'error': 'Only approved requests can be marked as returned'}), 400
        
        # Mark as returned
        query_db(
            '''UPDATE borrowing_requests 
               SET status = 'returned', return_date = CURRENT_TIMESTAMP
               WHERE id = %s''',
            (request_id,)
        )
        
        return jsonify({'message': 'Equipment marked as returned successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

