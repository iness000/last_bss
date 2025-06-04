from flask import Blueprint, request, jsonify
from models import db, BatteryHealthLog, Battery

battery_health_log_bp = Blueprint('battery_health_log', __name__)

@battery_health_log_bp.route('/battery_health_logs', methods=['POST'])
def create_battery_health_log():
    data = request.get_json()
    if not data or not data.get('battery_id'):
        return jsonify({"error": "Missing required field: battery_id"}), 400
    
    battery = Battery.query.get(data['battery_id'])
    if not battery:
        return jsonify({"error": f"Battery with id {data['battery_id']} not found"}), 404

    new_log = BatteryHealthLog(
        battery_id=data['battery_id'],
        soh_percent=data.get('soh_percent'),
        pack_voltage=data.get('pack_voltage'),
        cell_voltage_min=data.get('cell_voltage_min'),
        cell_voltage_max=data.get('cell_voltage_max'),
        cell_voltage_diff=data.get('cell_voltage_diff'),
        max_temp=data.get('max_temp'),
        ambient_temp=data.get('ambient_temp'),
        humidity=data.get('humidity'),
        internal_resist=data.get('internal_resist'),
        cycle_count=data.get('cycle_count'),
        error_code=data.get('error_code')
    )
    db.session.add(new_log)
    db.session.commit()
    return jsonify({"message": "BatteryHealthLog created successfully", "log_id": new_log.id}), 201

@battery_health_log_bp.route('/battery_health_logs', methods=['GET'])
def get_battery_health_logs():
    logs = BatteryHealthLog.query.all()
    return jsonify([{
        "id": log.id,
        "battery_id": log.battery_id,
        "soh_percent": log.soh_percent,
        "pack_voltage": log.pack_voltage,
        "cell_voltage_min": log.cell_voltage_min,
        "cell_voltage_max": log.cell_voltage_max,
        "cell_voltage_diff": log.cell_voltage_diff,
        "max_temp": log.max_temp,
        "ambient_temp": log.ambient_temp,
        "humidity": log.humidity,
        "internal_resist": log.internal_resist,
        "cycle_count": log.cycle_count,
        "error_code": log.error_code,
        "created_at": str(log.created_at),
        "battery_serial": log.battery.serial_number if log.battery else None
    } for log in logs])

@battery_health_log_bp.route('/battery_health_logs/<int:log_id>', methods=['GET'])
def get_battery_health_log(log_id):
    log = BatteryHealthLog.query.get_or_404(log_id)
    return jsonify({
        "id": log.id,
        "battery_id": log.battery_id,
        "soh_percent": log.soh_percent,
        "pack_voltage": log.pack_voltage,
        "cell_voltage_min": log.cell_voltage_min,
        "cell_voltage_max": log.cell_voltage_max,
        "cell_voltage_diff": log.cell_voltage_diff,
        "max_temp": log.max_temp,
        "ambient_temp": log.ambient_temp,
        "humidity": log.humidity,
        "internal_resist": log.internal_resist,
        "cycle_count": log.cycle_count,
        "error_code": log.error_code,
        "created_at": str(log.created_at),
        "battery_serial": log.battery.serial_number if log.battery else None
    })

@battery_health_log_bp.route('/battery_health_logs/<int:log_id>', methods=['PUT'])
def update_battery_health_log(log_id):
    log = BatteryHealthLog.query.get_or_404(log_id)
    data = request.get_json()

    if 'battery_id' in data:
        battery = Battery.query.get(data['battery_id'])
        if not battery:
            return jsonify({"error": f"Battery with id {data['battery_id']} not found"}), 404
        log.battery_id = data['battery_id']

    log.soh_percent = data.get('soh_percent', log.soh_percent)
    log.pack_voltage = data.get('pack_voltage', log.pack_voltage)
    log.cell_voltage_min = data.get('cell_voltage_min', log.cell_voltage_min)
    log.cell_voltage_max = data.get('cell_voltage_max', log.cell_voltage_max)
    log.cell_voltage_diff = data.get('cell_voltage_diff', log.cell_voltage_diff)
    log.max_temp = data.get('max_temp', log.max_temp)
    log.ambient_temp = data.get('ambient_temp', log.ambient_temp)
    log.humidity = data.get('humidity', log.humidity)
    log.internal_resist = data.get('internal_resist', log.internal_resist)
    log.cycle_count = data.get('cycle_count', log.cycle_count)
    log.error_code = data.get('error_code', log.error_code)
    
    db.session.commit()
    return jsonify({"message": "BatteryHealthLog updated successfully"})

@battery_health_log_bp.route('/battery_health_logs/<int:log_id>', methods=['DELETE'])
def delete_battery_health_log(log_id):
    log = BatteryHealthLog.query.get_or_404(log_id)
    db.session.delete(log)
    db.session.commit()
    return jsonify({"message": "BatteryHealthLog deleted successfully"})

@battery_health_log_bp.route('/batteries/<int:battery_id>/health_logs', methods=['GET'])
def get_battery_health_logs_by_battery(battery_id):
    battery = Battery.query.get_or_404(battery_id)
    logs = BatteryHealthLog.query.filter_by(battery_id=battery_id).all()
    return jsonify([{
        "id": log.id,
        "battery_id": log.battery_id,
        "soh_percent": log.soh_percent,
        "pack_voltage": log.pack_voltage,
        "cell_voltage_min": log.cell_voltage_min,
        "cell_voltage_max": log.cell_voltage_max,
        "cell_voltage_diff": log.cell_voltage_diff,
        "max_temp": log.max_temp,
        "ambient_temp": log.ambient_temp,
        "humidity": log.humidity,
        "internal_resist": log.internal_resist,
        "cycle_count": log.cycle_count,
        "error_code": log.error_code,
        "created_at": str(log.created_at)
    } for log in logs])
