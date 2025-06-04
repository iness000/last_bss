from flask import Blueprint, request, jsonify
from models import db, Station

station_bp = Blueprint('station', __name__)

@station_bp.route('/stations', methods=['POST'])
def create_station():
    data = request.get_json()
    if not data or not data.get('name'):
        return jsonify({"error": "Missing required field: name"}), 400
    
    new_station = Station(
        location=data.get('location'),
        name=data['name']
    )
    db.session.add(new_station)
    db.session.commit()
    return jsonify({"message": "Station created successfully", "station_id": new_station.id}), 201

@station_bp.route('/stations', methods=['GET'])
def get_stations():
    stations = Station.query.all()
    return jsonify([{
        "id": station.id,
        "location": station.location,
        "name": station.name,
        "created_at": str(station.created_at),
        "updated_at": str(station.updated_at)
    } for station in stations])

@station_bp.route('/stations/<int:station_id>', methods=['GET'])
def get_station(station_id):
    station = Station.query.get_or_404(station_id)
    return jsonify({
        "id": station.id,
        "location": station.location,
        "name": station.name,
        "created_at": str(station.created_at),
        "updated_at": str(station.updated_at)
    })

@station_bp.route('/stations/<int:station_id>', methods=['PUT'])
def update_station(station_id):
    station = Station.query.get_or_404(station_id)
    data = request.get_json()

    station.location = data.get('location', station.location)
    station.name = data.get('name', station.name)
    
    db.session.commit()
    return jsonify({"message": "Station updated successfully"})

@station_bp.route('/stations/<int:station_id>', methods=['DELETE'])
def delete_station(station_id):
    station = Station.query.get_or_404(station_id)
    db.session.delete(station)
    db.session.commit()
    return jsonify({"message": "Station deleted successfully"})

@station_bp.route('/stations/<int:station_id>/batteries', methods=['GET'])
def get_station_batteries(station_id):
    station = Station.query.get_or_404(station_id)
    batteries = station.batteries
    return jsonify([{
        "id": battery.id,
        "status": battery.status,
        "serial_number": battery.serial_number,
        "battery_type": battery.battery_type,
        "battery_capacity": battery.battery_capacity,
        "manufacture_date": str(battery.manufacture_date) if battery.manufacture_date else None,
        "created_at": str(battery.created_at),
        "updated_at": str(battery.updated_at)
    } for battery in batteries])

@station_bp.route('/stations/<int:station_id>/slots', methods=['GET'])
def get_station_slots(station_id):
    station = Station.query.get_or_404(station_id)
    slots = station.slots
    return jsonify([{
        "id": slot.id,
        "slot_number": slot.slot_number,
        "battery_id": slot.battery_id,
        "status": slot.status,
        "is_charging": slot.is_charging,
        "last_updated": str(slot.last_updated)
    } for slot in slots])
