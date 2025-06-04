from flask import Blueprint, request, jsonify
from models import db, Swap, User, Battery, Station

swap_bp = Blueprint('swap', __name__)

@swap_bp.route('/swaps', methods=['POST'])
def create_swap():
    data = request.get_json()
    if not data or not data.get('user_id'):
        return jsonify({"error": "Missing required field: user_id"}), 400
    
    user = User.query.get(data['user_id'])
    if not user:
        return jsonify({"error": f"User with id {data['user_id']} not found"}), 404

    if data.get('issued_battery_id'):
        issued_battery = Battery.query.get(data['issued_battery_id'])
        if not issued_battery:
            return jsonify({"error": f"Issued battery with id {data['issued_battery_id']} not found"}), 404

    if data.get('returned_battery_id'):
        returned_battery = Battery.query.get(data['returned_battery_id'])
        if not returned_battery:
            return jsonify({"error": f"Returned battery with id {data['returned_battery_id']} not found"}), 404

    if data.get('pickup_station_id'):
        pickup_station = Station.query.get(data['pickup_station_id'])
        if not pickup_station:
            return jsonify({"error": f"Pickup station with id {data['pickup_station_id']} not found"}), 404

    if data.get('deposit_station_id'):
        deposit_station = Station.query.get(data['deposit_station_id'])
        if not deposit_station:
            return jsonify({"error": f"Deposit station with id {data['deposit_station_id']} not found"}), 404

    new_swap = Swap(
        issued_battery_id=data.get('issued_battery_id'),
        returned_battery_id=data.get('returned_battery_id'),
        user_id=data['user_id'],
        pickup_station_id=data.get('pickup_station_id'),
        deposit_station_id=data.get('deposit_station_id'),
        start_time=data.get('start_time'),
        end_time=data.get('end_time'),
        battery_percentage_start=data.get('battery_percentage_start'),
        battery_percentage_end=data.get('battery_percentage_end'),
        ah_used=data.get('ah_used')
    )
    db.session.add(new_swap)
    db.session.commit()
    return jsonify({"message": "Swap created successfully", "swap_id": new_swap.id}), 201

@swap_bp.route('/swaps', methods=['GET'])
def get_swaps():
    swaps = Swap.query.all()
    return jsonify([{
        "id": swap.id,
        "issued_battery_id": swap.issued_battery_id,
        "returned_battery_id": swap.returned_battery_id,
        "user_id": swap.user_id,
        "pickup_station_id": swap.pickup_station_id,
        "deposit_station_id": swap.deposit_station_id,
        "start_time": str(swap.start_time) if swap.start_time else None,
        "end_time": str(swap.end_time) if swap.end_time else None,
        "battery_percentage_start": swap.battery_percentage_start,
        "battery_percentage_end": swap.battery_percentage_end,
        "ah_used": swap.ah_used,
        "created_at": str(swap.created_at),
        "updated_at": str(swap.updated_at),
        "user_name": swap.user.name if swap.user else None,
        "user_email": swap.user.email if swap.user else None
    } for swap in swaps])

@swap_bp.route('/swaps/<int:swap_id>', methods=['GET'])
def get_swap(swap_id):
    swap = Swap.query.get_or_404(swap_id)
    return jsonify({
        "id": swap.id,
        "issued_battery_id": swap.issued_battery_id,
        "returned_battery_id": swap.returned_battery_id,
        "user_id": swap.user_id,
        "pickup_station_id": swap.pickup_station_id,
        "deposit_station_id": swap.deposit_station_id,
        "start_time": str(swap.start_time) if swap.start_time else None,
        "end_time": str(swap.end_time) if swap.end_time else None,
        "battery_percentage_start": swap.battery_percentage_start,
        "battery_percentage_end": swap.battery_percentage_end,
        "ah_used": swap.ah_used,
        "created_at": str(swap.created_at),
        "updated_at": str(swap.updated_at),
        "user_name": swap.user.name if swap.user else None,
        "user_email": swap.user.email if swap.user else None
    })

@swap_bp.route('/swaps/<int:swap_id>', methods=['PUT'])
def update_swap(swap_id):
    swap = Swap.query.get_or_404(swap_id)
    data = request.get_json()

    if 'user_id' in data:
        user = User.query.get(data['user_id'])
        if not user:
            return jsonify({"error": f"User with id {data['user_id']} not found"}), 404
        swap.user_id = data['user_id']

    if 'issued_battery_id' in data and data['issued_battery_id'] is not None:
        issued_battery = Battery.query.get(data['issued_battery_id'])
        if not issued_battery:
            return jsonify({"error": f"Issued battery with id {data['issued_battery_id']} not found"}), 404
        swap.issued_battery_id = data['issued_battery_id']
    elif 'issued_battery_id' in data and data['issued_battery_id'] is None:
        swap.issued_battery_id = None

    if 'returned_battery_id' in data and data['returned_battery_id'] is not None:
        returned_battery = Battery.query.get(data['returned_battery_id'])
        if not returned_battery:
            return jsonify({"error": f"Returned battery with id {data['returned_battery_id']} not found"}), 404
        swap.returned_battery_id = data['returned_battery_id']
    elif 'returned_battery_id' in data and data['returned_battery_id'] is None:
        swap.returned_battery_id = None

    if 'pickup_station_id' in data and data['pickup_station_id'] is not None:
        pickup_station = Station.query.get(data['pickup_station_id'])
        if not pickup_station:
            return jsonify({"error": f"Pickup station with id {data['pickup_station_id']} not found"}), 404
        swap.pickup_station_id = data['pickup_station_id']
    elif 'pickup_station_id' in data and data['pickup_station_id'] is None:
        swap.pickup_station_id = None

    if 'deposit_station_id' in data and data['deposit_station_id'] is not None:
        deposit_station = Station.query.get(data['deposit_station_id'])
        if not deposit_station:
            return jsonify({"error": f"Deposit station with id {data['deposit_station_id']} not found"}), 404
        swap.deposit_station_id = data['deposit_station_id']
    elif 'deposit_station_id' in data and data['deposit_station_id'] is None:
        swap.deposit_station_id = None

    swap.start_time = data.get('start_time', swap.start_time)
    swap.end_time = data.get('end_time', swap.end_time)
    swap.battery_percentage_start = data.get('battery_percentage_start', swap.battery_percentage_start)
    swap.battery_percentage_end = data.get('battery_percentage_end', swap.battery_percentage_end)
    swap.ah_used = data.get('ah_used', swap.ah_used)
    
    db.session.commit()
    return jsonify({"message": "Swap updated successfully"})

@swap_bp.route('/swaps/<int:swap_id>', methods=['DELETE'])
def delete_swap(swap_id):
    swap = Swap.query.get_or_404(swap_id)
    db.session.delete(swap)
    db.session.commit()
    return jsonify({"message": "Swap deleted successfully"})

@swap_bp.route('/users/<int:user_id>/swaps', methods=['GET'])
def get_user_swaps(user_id):
    user = User.query.get_or_404(user_id)
    swaps = Swap.query.filter_by(user_id=user_id).all()
    return jsonify([{
        "id": swap.id,
        "issued_battery_id": swap.issued_battery_id,
        "returned_battery_id": swap.returned_battery_id,
        "pickup_station_id": swap.pickup_station_id,
        "deposit_station_id": swap.deposit_station_id,
        "start_time": str(swap.start_time) if swap.start_time else None,
        "end_time": str(swap.end_time) if swap.end_time else None,
        "battery_percentage_start": swap.battery_percentage_start,
        "battery_percentage_end": swap.battery_percentage_end,
        "ah_used": swap.ah_used,
        "created_at": str(swap.created_at),
        "updated_at": str(swap.updated_at)
    } for swap in swaps])
