from flask import Blueprint, request, jsonify
from models import db, RFIDCard, User

rfid_card_bp = Blueprint('rfid_card', __name__)

@rfid_card_bp.route('/rfid_cards', methods=['POST'])
def create_rfid_card():
    data = request.get_json()
    if not data or not data.get('user_id') or not data.get('rfid_code'):
        return jsonify({"error": "Missing required fields: user_id, rfid_code"}), 400
    
    user = User.query.get(data['user_id'])
    if not user:
        return jsonify({"error": f"User with id {data['user_id']} not found"}), 404

    new_card = RFIDCard(
        user_id=data['user_id'],
        rfid_code=data['rfid_code'],
        assigned_battery_id=data.get('assigned_battery_id'),
        status=data.get('status', 'active')
    )
    db.session.add(new_card)
    db.session.commit()
    return jsonify({"message": "RFIDCard created successfully", "card_id": new_card.id}), 201

@rfid_card_bp.route('/rfid_cards', methods=['GET'])
def get_rfid_cards():
    cards = RFIDCard.query.all()
    return jsonify([{
        "id": card.id, "user_id": card.user_id, "rfid_code": card.rfid_code,
        "assigned_battery_id": card.assigned_battery_id,
        "issued_at": str(card.issued_at) if card.issued_at else None,
        "status": card.status,
        "user_email": card.user.email if card.user else None
    } for card in cards])

@rfid_card_bp.route('/rfid_cards/by_code/<string:rfid_code>', methods=['GET'])
def get_rfid_card_by_code(rfid_code):
    card = RFIDCard.query.filter_by(rfid_code=rfid_code).first()
    if not card:
        return jsonify({"error": "RFID card not found"}), 404
    
    return jsonify({
        "id": card.id, "user_id": card.user_id, "rfid_code": card.rfid_code,
        "assigned_battery_id": card.assigned_battery_id,
        "issued_at": str(card.issued_at) if card.issued_at else None,
        "status": card.status,
        "user_email": card.user.email if card.user else None
    })

@rfid_card_bp.route('/rfid_cards/<int:card_id>', methods=['GET'])
def get_rfid_card(card_id):
    card = RFIDCard.query.get_or_404(card_id)
    return jsonify({
        "id": card.id, "user_id": card.user_id, "rfid_code": card.rfid_code,
        "assigned_battery_id": card.assigned_battery_id,
        "issued_at": str(card.issued_at) if card.issued_at else None,
        "status": card.status,
        "user_email": card.user.email if card.user else None
    })

@rfid_card_bp.route('/rfid_cards/<int:card_id>', methods=['PUT'])
def update_rfid_card(card_id):
    card = RFIDCard.query.get_or_404(card_id)
    data = request.get_json()

    if 'user_id' in data:
        user = User.query.get(data['user_id'])
        if not user:
            return jsonify({"error": f"User with id {data['user_id']} not found"}), 404
        card.user_id = data['user_id']
    
    card.rfid_code = data.get('rfid_code', card.rfid_code)
    card.assigned_battery_id = data.get('assigned_battery_id', card.assigned_battery_id)
    card.status = data.get('status', card.status)
    
    db.session.commit()
    return jsonify({"message": "RFIDCard updated successfully"})

@rfid_card_bp.route('/rfid_cards/<int:card_id>', methods=['DELETE'])
def delete_rfid_card(card_id):
    card = RFIDCard.query.get_or_404(card_id)
    db.session.delete(card)
    db.session.commit()
    return jsonify({"message": "RFIDCard deleted successfully"})