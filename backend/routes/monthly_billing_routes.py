from flask import Blueprint, request, jsonify
from models import db, MonthlyBilling, User

monthly_billing_bp = Blueprint('monthly_billing', __name__)

@monthly_billing_bp.route('/monthly_billings', methods=['POST'])
def create_monthly_billing():
    data = request.get_json()
    if not data or not data.get('user_id') or not data.get('billing_month'):
        return jsonify({"error": "Missing required fields: user_id, billing_month"}), 400
    
    user = User.query.get(data['user_id'])
    if not user:
        return jsonify({"error": f"User with id {data['user_id']} not found"}), 404

    new_billing = MonthlyBilling(
        user_id=data['user_id'],
        billing_month=data['billing_month'],
        total_ah_used=data.get('total_ah_used'),
        ah_included=data.get('ah_included'),
        ah_excess=data.get('ah_excess'),
        total_amount_due=data.get('total_amount_due'),
        paid_amount=data.get('paid_amount'),
        payment_status=data.get('payment_status'),
        payment_date=data.get('payment_date')
    )
    db.session.add(new_billing)
    db.session.commit()
    return jsonify({"message": "MonthlyBilling created successfully", "billing_id": new_billing.id}), 201

@monthly_billing_bp.route('/monthly_billings', methods=['GET'])
def get_monthly_billings():
    billings = MonthlyBilling.query.all()
    return jsonify([{
        "id": billing.id,
        "user_id": billing.user_id,
        "billing_month": billing.billing_month,
        "total_ah_used": billing.total_ah_used,
        "ah_included": billing.ah_included,
        "ah_excess": billing.ah_excess,
        "total_amount_due": billing.total_amount_due,
        "paid_amount": billing.paid_amount,
        "payment_status": billing.payment_status,
        "payment_date": str(billing.payment_date) if billing.payment_date else None,
        "created_at": str(billing.created_at),
        "user_name": billing.user.name if billing.user else None,
        "user_email": billing.user.email if billing.user else None
    } for billing in billings])

@monthly_billing_bp.route('/monthly_billings/<int:billing_id>', methods=['GET'])
def get_monthly_billing(billing_id):
    billing = MonthlyBilling.query.get_or_404(billing_id)
    return jsonify({
        "id": billing.id,
        "user_id": billing.user_id,
        "billing_month": billing.billing_month,
        "total_ah_used": billing.total_ah_used,
        "ah_included": billing.ah_included,
        "ah_excess": billing.ah_excess,
        "total_amount_due": billing.total_amount_due,
        "paid_amount": billing.paid_amount,
        "payment_status": billing.payment_status,
        "payment_date": str(billing.payment_date) if billing.payment_date else None,
        "created_at": str(billing.created_at),
        "user_name": billing.user.name if billing.user else None,
        "user_email": billing.user.email if billing.user else None
    })

@monthly_billing_bp.route('/monthly_billings/<int:billing_id>', methods=['PUT'])
def update_monthly_billing(billing_id):
    billing = MonthlyBilling.query.get_or_404(billing_id)
    data = request.get_json()

    if 'user_id' in data:
        user = User.query.get(data['user_id'])
        if not user:
            return jsonify({"error": f"User with id {data['user_id']} not found"}), 404
        billing.user_id = data['user_id']

    billing.billing_month = data.get('billing_month', billing.billing_month)
    billing.total_ah_used = data.get('total_ah_used', billing.total_ah_used)
    billing.ah_included = data.get('ah_included', billing.ah_included)
    billing.ah_excess = data.get('ah_excess', billing.ah_excess)
    billing.total_amount_due = data.get('total_amount_due', billing.total_amount_due)
    billing.paid_amount = data.get('paid_amount', billing.paid_amount)
    billing.payment_status = data.get('payment_status', billing.payment_status)
    billing.payment_date = data.get('payment_date', billing.payment_date)
    
    db.session.commit()
    return jsonify({"message": "MonthlyBilling updated successfully"})

@monthly_billing_bp.route('/monthly_billings/<int:billing_id>', methods=['DELETE'])
def delete_monthly_billing(billing_id):
    billing = MonthlyBilling.query.get_or_404(billing_id)
    db.session.delete(billing)
    db.session.commit()
    return jsonify({"message": "MonthlyBilling deleted successfully"})

@monthly_billing_bp.route('/users/<int:user_id>/monthly_billings', methods=['GET'])
def get_user_monthly_billings(user_id):
    user = User.query.get_or_404(user_id)
    billings = MonthlyBilling.query.filter_by(user_id=user_id).all()
    return jsonify([{
        "id": billing.id,
        "billing_month": billing.billing_month,
        "total_ah_used": billing.total_ah_used,
        "ah_included": billing.ah_included,
        "ah_excess": billing.ah_excess,
        "total_amount_due": billing.total_amount_due,
        "paid_amount": billing.paid_amount,
        "payment_status": billing.payment_status,
        "payment_date": str(billing.payment_date) if billing.payment_date else None,
        "created_at": str(billing.created_at)
    } for billing in billings])

@monthly_billing_bp.route('/monthly_billings/<int:billing_id>/mark_paid', methods=['POST'])
def mark_billing_paid(billing_id):
    billing = MonthlyBilling.query.get_or_404(billing_id)
    data = request.get_json()
    
    billing.payment_status = 'paid'
    billing.paid_amount = data.get('paid_amount', billing.total_amount_due)
    billing.payment_date = data.get('payment_date')
    
    db.session.commit()
    return jsonify({"message": "Billing marked as paid successfully"})

@monthly_billing_bp.route('/monthly_billings/unpaid', methods=['GET'])
def get_unpaid_billings():
    unpaid_billings = MonthlyBilling.query.filter(
        MonthlyBilling.payment_status.in_(['unpaid', 'pending', None])
    ).all()
    return jsonify([{
        "id": billing.id,
        "user_id": billing.user_id,
        "billing_month": billing.billing_month,
        "total_ah_used": billing.total_ah_used,
        "ah_included": billing.ah_included,
        "ah_excess": billing.ah_excess,
        "total_amount_due": billing.total_amount_due,
        "paid_amount": billing.paid_amount,
        "payment_status": billing.payment_status,
        "payment_date": str(billing.payment_date) if billing.payment_date else None,
        "created_at": str(billing.created_at),
        "user_name": billing.user.name if billing.user else None,
        "user_email": billing.user.email if billing.user else None
    } for billing in unpaid_billings])
