from flask import Blueprint, request, jsonify
from models import db, SubscriptionPlan

subscription_plan_bp = Blueprint('subscription_plan', __name__)

@subscription_plan_bp.route('/subscription_plans', methods=['POST'])
def create_subscription_plan():
    data = request.get_json()
    if not data or not data.get('name'):
        return jsonify({"error": "Missing required field: name"}), 400
    
    new_plan = SubscriptionPlan(
        name=data['name'],
        monthly_fee=data.get('monthly_fee'),
        included_ah=data.get('included_ah'),
        extra_ah_rate=data.get('extra_ah_rate')
    )
    db.session.add(new_plan)
    db.session.commit()
    return jsonify({"message": "SubscriptionPlan created successfully", "plan_id": new_plan.id}), 201

@subscription_plan_bp.route('/subscription_plans', methods=['GET'])
def get_subscription_plans():
    plans = SubscriptionPlan.query.all()
    return jsonify([{
        "id": plan.id,
        "name": plan.name,
        "monthly_fee": plan.monthly_fee,
        "included_ah": plan.included_ah,
        "extra_ah_rate": plan.extra_ah_rate
    } for plan in plans])

@subscription_plan_bp.route('/subscription_plans/<int:plan_id>', methods=['GET'])
def get_subscription_plan(plan_id):
    plan = SubscriptionPlan.query.get_or_404(plan_id)
    return jsonify({
        "id": plan.id,
        "name": plan.name,
        "monthly_fee": plan.monthly_fee,
        "included_ah": plan.included_ah,
        "extra_ah_rate": plan.extra_ah_rate
    })

@subscription_plan_bp.route('/subscription_plans/<int:plan_id>', methods=['PUT'])
def update_subscription_plan(plan_id):
    plan = SubscriptionPlan.query.get_or_404(plan_id)
    data = request.get_json()

    plan.name = data.get('name', plan.name)
    plan.monthly_fee = data.get('monthly_fee', plan.monthly_fee)
    plan.included_ah = data.get('included_ah', plan.included_ah)
    plan.extra_ah_rate = data.get('extra_ah_rate', plan.extra_ah_rate)
    
    db.session.commit()
    return jsonify({"message": "SubscriptionPlan updated successfully"})

@subscription_plan_bp.route('/subscription_plans/<int:plan_id>', methods=['DELETE'])
def delete_subscription_plan(plan_id):
    plan = SubscriptionPlan.query.get_or_404(plan_id)
    db.session.delete(plan)
    db.session.commit()
    return jsonify({"message": "SubscriptionPlan deleted successfully"})
