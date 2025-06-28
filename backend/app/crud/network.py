from sqlalchemy.orm import Session
from app.db.models.network import Network
from app.schemas.network import NetworkCreate

def get_network(db: Session, network_id: int):
    return db.query(Network).filter(Network.id == network_id).first()

def get_networks_for_org(db: Session, organization_id: int, skip: int = 0, limit: int = 100):
    return db.query(Network).filter(Network.organization_id == organization_id).offset(skip).limit(limit).all()

def create_network(db: Session, network: NetworkCreate):
    db_network = Network(
        name=network.name,
        cidr=network.cidr,
        description=network.description,
        organization_id=network.organization_id,
    )
    db.add(db_network)
    db.commit()
    db.refresh(db_network)
    return db_network

def delete_network(db: Session, db_network: Network):
    db.delete(db_network)
    db.commit()
    return db_network
