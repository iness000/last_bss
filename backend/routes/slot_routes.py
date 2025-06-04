from flask import Blueprint, request, jsonify
from models import db, Slot, Station, Battery

slot_bp = Blueprint('slot', __name__)

@slot_bp.route('/slots', methods=['POST'])
def create_slot():
    data = request.get_json()
    if not data or not data.get('station_id') or not data.get('slot_number'):
        return jsonify({"error": "Missing required fields: station_id, slot_number"}), 400
    
    station = Station.query.get(data['station_id'])
    if not station:
        return jsonify({"error": f"Station with id {data['station_id']} not found"}), 404

    if data.get('battery_id'):
        battery = Battery.query.get(data['battery_id'])
        if not battery:
            return jsonify({"error": f"Battery with id {data['battery_id']} not found"}), 404

    new_slot = Slot(
        station_id=data['station_id'],
        slot_number=data['slot_number'],
        battery_id=data.get('battery_id'),
        status=data.get('status', 'empty'),
        is_charging=data.get('is_charging', False)
    )
    db.session.add(new_slot)
    db.session.commit()
    return jsonify({"message": "Slot created successfully", "slot_id": new_slot.id}), 201

@slot_bp.route('/slots', methods=['GET'])
def get_slots():
    slots = Slot.query.all()
    return jsonify([{
        "id": slot.id,
        "station_id": slot.station_id,
        "slot_number": slot.slot_number,
        "battery_id": slot.battery_id,
        "status": slot.status,
        "is_charging": slot.is_charging,
        "last_updated": str(slot.last_updated),
        "station_name": slot.station.name if slot.station else None,
        "battery_serial": slot.battery.serial_number if slot.battery else None
    } for slot in slots])

@slot_bp.route('/slots/<int:slot_id>', methods=['GET'])
def get_slot(slot_id):
    slot = Slot.query.get_or_404(slot_id)
    return jsonify({
        "id": slot.id,
        "station_id": slot.station_id,
        "slot_number": slot.slot_number,
        "battery_id": slot.battery_id,
        "status": slot.status,
        "is_charging": slot.is_charging,
        "last_updated": str(slot.last_updated),
        "station_name": slot.station.name if slot.station else None,
        "battery_serial": slot.battery.serial_number if slot.battery else None
    })

@slot_bp.route('/slots/<int:slot_id>', methods=['PUT'])
def update_slot(slot_id):
    slot = Slot.query.get_or_404(slot_id)
    data = request.get_json()

    if 'station_id' in data:
        station = Station.query.get(data['station_id'])
        if not station:
            return jsonify({"error": f"Station with id {data['station_id']} not found"}), 404
        slot.station_id = data['station_id']

    if 'battery_id' in data and data['battery_id'] is not None:
        battery = Battery.query.get(data['battery_id'])
        if not battery:
            return jsonify({"error": f"Battery with id {data['battery_id']} not found"}), 404
        slot.battery_id = data['battery_id']
    elif 'battery_id' in data and data['battery_id'] is None:
        slot.battery_id = None

    slot.slot_number = data.get('slot_number', slot.slot_number)
    slot.status = data.get('status', slot.status)
    slot.is_charging = data.get('is_charging', slot.is_charging)
    
    db.session.commit()
    return jsonify({"message": "Slot updated successfully"})

@slot_bp.route('/slots/<int:slot_id>', methods=['DELETE'])
def delete_slot(slot_id):
    slot = Slot.query.get_or_404(slot_id)
    db.session.delete(slot)
    db.session.commit()
    return jsonify({"message": "Slot deleted successfully"})

@slot_bp.route('/slots/<int:slot_id>/assign_battery', methods=['POST'])
def assign_battery_to_slot(slot_id):
    slot = Slot.query.get_or_404(slot_id)
    data = request.get_json()
    
    if not data or not data.get('battery_id'):
        return jsonify({"error": "Missing required field: battery_id"}), 400
    
    battery = Battery.query.get(data['battery_id'])
    if not battery:
        return jsonify({"error": f"Battery with id {data['battery_id']} not found"}), 404
    
    slot.battery_id = data['battery_id']
    slot.status = 'occupied'
    db.session.commit()
    return jsonify({"message": "Battery assigned to slot successfully"})

@slot_bp.route('/slots/<int:slot_id>/remove_battery', methods=['POST'])
def remove_battery_from_slot(slot_id):
    slot = Slot.query.get_or_404(slot_id)
    slot.battery_id = None
    slot.status = 'empty'
    slot.is_charging = False
    db.session.commit()
    return jsonify({"message": "Battery removed from slot successfully"})
