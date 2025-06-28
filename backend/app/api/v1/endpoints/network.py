from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.network import NetworkOut, NetworkCreate
from app.crud.network import get_network, get_networks_for_org, create_network, delete_network
from app.api.deps import get_db

router = APIRouter()

@router.get("/", response_model=List[NetworkOut])
def list_networks(organization_id: int, db: Session = Depends(get_db)):
    return get_networks_for_org(db, organization_id=organization_id)

@router.get("/{network_id}", response_model=NetworkOut)
def retrieve_network(network_id: int, db: Session = Depends(get_db)):
    network = get_network(db, network_id)
    if not network:
        raise HTTPException(status_code=404, detail="Network not found")
    return network

@router.post("/", response_model=NetworkOut)
def create_network_api(network_in: NetworkCreate, db: Session = Depends(get_db)):
    return create_network(db, network=network_in)

@router.delete("/{network_id}")
def delete_network_api(network_id: int, db: Session = Depends(get_db)):
    db_network = get_network(db, network_id)
    if not db_network:
        raise HTTPException(status_code=404, detail="Network not found")
    return delete_network(db, db_network)
