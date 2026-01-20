# backend/rni_web/src/sinapsis/schemas.py

from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel


# ============================
# PERSONAS
# ============================

class PersonnelSchema(BaseModel):
    _id: str
    name: str


# ============================
# EQUIPOS
# ============================

class TeamMemberSchema(BaseModel):
    personnel: PersonnelSchema
    role: str


class TeamSchema(BaseModel):
    _id: str
    name: str
    description: Optional[str] = None
    coordinator: Optional[PersonnelSchema] = None
    members: List[TeamMemberSchema] = []
    organizational_unit_code: Optional[str] = None
    organizational_path: Optional[str] = None


# ============================
# REPOSITORIOS / TRACKING
# ============================

class RepositorySchema(BaseModel):
    name: str
    url: str


class IssueTrackerSchema(BaseModel):
    provider: str
    project_url: str
    config: Optional[Dict[str, Any]] = None


# ============================
# PROYECTO PRINCIPAL
# ============================

class SinapsisProjectSchema(BaseModel):
    _id: str
    name: str
    description: Optional[str] = None

    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

    status: Optional[str] = None
    category: Optional[str] = None
    lifecycle_stage: Optional[str] = None

    tech_domain: List[str] = []
    service_tier: Optional[str] = None
    methodology: Optional[str] = None
    sprint_length_days: Optional[int] = None
    release_cycle: Optional[str] = None
    initiative_level: Optional[str] = None
    architecture_style: Optional[str] = None
    risk_level: Optional[str] = None

    compliance: List[str] = []

    repositories: List[RepositorySchema] = []
    issue_tracker: Optional[IssueTrackerSchema] = None

    okrs: Optional[Any] = None
    quality_metrics: Optional[Any] = None

    stakeholders: List[Any] = []
    teams: List[TeamSchema] = []

    class Config:
        extra = "allow"  # tolera campos nuevos sin romper
