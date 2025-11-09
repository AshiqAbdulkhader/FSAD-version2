from flask import Blueprint, request, jsonify
from config.database import query_db
from middleware.auth import token_required, role_required

bp = Blueprint('equipment', __name__)

@bp.route('', methods=['GET'])
@token_required
def get_equipment():
    """Get all equipment with optional filters"""
    try:
        category = request.args.get('category')
        search = request.args.get('search')
        
        query = 'SELECT id, name, category, condition, quantity, description FROM equipment WHERE 1=1'
        params = []
        
        if category:
            query += ' AND category = %s'
            params.append(category)
        
        if search:
            query += ' AND (name ILIKE %s OR description ILIKE %s)'
            params.extend([f'%{search}%', f'%{search}%'])
        
        query += ' ORDER BY name'
        
        equipment_list = query_db(query, tuple(params), fetch_all=True)
        
        result = []
        for item in equipment_list:
            # Check availability (count active borrowings)
            active_borrowings = query_db(
                '''SELECT COUNT(*) FROM borrowing_requests 
                   WHERE equipment_id = %s AND status = 'approved' 
                   AND CURRENT_DATE BETWEEN start_date AND end_date''',
                (item[0],),
                fetch_one=True
            )
            active_count = active_borrowings[0] if active_borrowings else 0
            available = max(0, item[4] - active_count)
            
            result.append({
                'id': item[0],
                'name': item[1],
                'category': item[2],
                'condition': item[3],
                'quantity': item[4],
                'available': available,
                'description': item[5]
            })
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:equipment_id>', methods=['GET'])
@token_required
def get_equipment_by_id(equipment_id):
    """Get single equipment by ID"""
    try:
        equipment = query_db(
            'SELECT id, name, category, condition, quantity, description FROM equipment WHERE id = %s',
            (equipment_id,),
            fetch_one=True
        )
        
        if not equipment:
            return jsonify({'error': 'Equipment not found'}), 404
        
        # Check availability
        active_borrowings = query_db(
            '''SELECT COUNT(*) FROM borrowing_requests 
               WHERE equipment_id = %s AND status = 'approved' 
               AND CURRENT_DATE BETWEEN start_date AND end_date''',
            (equipment_id,),
            fetch_one=True
        )
        active_count = active_borrowings[0] if active_borrowings else 0
        available = max(0, equipment[4] - active_count)
        
        return jsonify({
            'id': equipment[0],
            'name': equipment[1],
            'category': equipment[2],
            'condition': equipment[3],
            'quantity': equipment[4],
            'available': available,
            'description': equipment[5]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('', methods=['POST'])
@role_required('admin')
def create_equipment():
    """Create new equipment (admin only)"""
    try:
        data = request.get_json()
        name = data.get('name')
        category = data.get('category')
        condition = data.get('condition')
        quantity = data.get('quantity', 1)
        description = data.get('description', '')
        
        if not all([name, category, condition]):
            return jsonify({'error': 'Name, category, and condition are required'}), 400
        
        if condition not in ['excellent', 'good', 'fair', 'poor']:
            return jsonify({'error': 'Invalid condition'}), 400
        
        query_db(
            'INSERT INTO equipment (name, category, condition, quantity, description) VALUES (%s, %s, %s, %s, %s)',
            (name, category, condition, quantity, description)
        )
        
        return jsonify({'message': 'Equipment created successfully'}), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:equipment_id>', methods=['PUT'])
@role_required('admin')
def update_equipment(equipment_id):
    """Update equipment (admin only)"""
    try:
        data = request.get_json()
        
        # Check if equipment exists
        equipment = query_db(
            'SELECT id FROM equipment WHERE id = %s',
            (equipment_id,),
            fetch_one=True
        )
        
        if not equipment:
            return jsonify({'error': 'Equipment not found'}), 404
        
        # Build update query dynamically
        updates = []
        params = []
        
        if 'name' in data:
            updates.append('name = %s')
            params.append(data['name'])
        if 'category' in data:
            updates.append('category = %s')
            params.append(data['category'])
        if 'condition' in data:
            if data['condition'] not in ['excellent', 'good', 'fair', 'poor']:
                return jsonify({'error': 'Invalid condition'}), 400
            updates.append('condition = %s')
            params.append(data['condition'])
        if 'quantity' in data:
            updates.append('quantity = %s')
            params.append(data['quantity'])
        if 'description' in data:
            updates.append('description = %s')
            params.append(data['description'])
        
        if not updates:
            return jsonify({'error': 'No fields to update'}), 400
        
        updates.append('updated_at = CURRENT_TIMESTAMP')
        params.append(equipment_id)
        
        query = f'UPDATE equipment SET {", ".join(updates)} WHERE id = %s'
        query_db(query, tuple(params))
        
        return jsonify({'message': 'Equipment updated successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:equipment_id>', methods=['DELETE'])
@role_required('admin')
def delete_equipment(equipment_id):
    """Delete equipment (admin only)"""
    try:
        # Check if equipment exists
        equipment = query_db(
            'SELECT id FROM equipment WHERE id = %s',
            (equipment_id,),
            fetch_one=True
        )
        
        if not equipment:
            return jsonify({'error': 'Equipment not found'}), 404
        
        query_db('DELETE FROM equipment WHERE id = %s', (equipment_id,))
        
        return jsonify({'message': 'Equipment deleted successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/categories', methods=['GET'])
@token_required
def get_categories():
    """Get all equipment categories"""
    try:
        categories = query_db(
            'SELECT DISTINCT category FROM equipment ORDER BY category',
            fetch_all=True
        )
        result = [cat[0] for cat in categories]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

