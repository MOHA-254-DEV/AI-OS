from sqlalchemy.orm import Session
from app.db.models.organization import Organization
from app.schemas.organization import OrganizationCreate, OrganizationUpdate

def get_organization(db: Session, org_id: int):
    return db.query(Organization).filter(Organization.id == org_id).first()

def get_organization_by_name(db: Session, name: str):
    return db.query(Organization).filter(Organization.name == name).first()

def get_organizations(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Organization).offset(skip).limit(limit).all()

def create_organization(db: Session, org: OrganizationCreate):
    db_org = Organization(
        name=org.name,
        display_name=org.display_name,
        description=org.description,
    )
    db.add(db_org)
    db.commit()
    db.refresh(db_org)
    return db_org

def update_organization(db: Session, db_org: Organization, org_update: OrganizationUpdate):
    for field, value in org_update.dict(exclude_unset=True).items():
        setattr(db_org, field, value)
    db.commit()
    db.refresh(db_org)
    return db_org

def delete_organization(db: Session, db_org: Organization):
    db.delete(db_org)
    db.commit()
    return db_org
