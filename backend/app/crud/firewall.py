from sqlalchemy.orm import Session
from typing import Optional, List
from app.db.models.firewall import FirewallRule
from app.schemas.firewall import FirewallRuleCreate, FirewallRuleUpdate

def get_rule(db: Session, rule_id):
    return db.query(FirewallRule).filter(FirewallRule.id == rule_id).first()

def get_rules(db: Session, skip: int = 0, limit: int = 100) -> List[FirewallRule]:
    return db.query(FirewallRule).offset(skip).limit(limit).all()

def create_rule(db: Session, rule: FirewallRuleCreate):
    db_rule = FirewallRule(**rule.dict())
    db.add(db_rule)
    db.commit()
    db.refresh(db_rule)
    return db_rule

def update_rule(db: Session, db_rule: FirewallRule, rule_update: FirewallRuleUpdate):
    for field, value in rule_update.dict(exclude_unset=True).items():
        setattr(db_rule, field, value)
    db.commit()
    db.refresh(db_rule)
    return db_rule

def delete_rule(db: Session, db_rule: FirewallRule):
    db.delete(db_rule)
    db.commit()
    return True
