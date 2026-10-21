import os
import pytest
from datetime import timedelta
import jwt
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.config import settings
from databases.session import Base, get_db
from databases.schema.models import User, Doctor, Manufacturer

# Use SQLite in-memory for testing
from sqlalchemy.pool import StaticPool

TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def setup_jwt_secret():
    # Ensure JWT secret is set for tests
    settings.JWT_SECRET_KEY = "testsecretkeyforunitandintegrationtestingatleast32charslong!"


@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_successful_doctor_registration(client):
    payload = {
        "email": "doctor.test@example.com",
        "password": "Password123!",
        "role": "doctor",
        "full_name_or_company": "Dr. Sarah Connor",
        "medical_license_or_contact_name": "MED-998877",
        "specialty_or_contact_email": "Cardiology",
    }
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "doctor.test@example.com"
    assert data["role"] == "doctor"
    assert "password" not in data
    assert "hashed_password" not in data


def test_duplicate_email_registration_rejected(client):
    payload = {
        "email": "duplicate@example.com",
        "password": "Password123!",
        "role": "doctor",
        "full_name_or_company": "Dr. First",
        "medical_license_or_contact_name": "MED-111111",
        "specialty_or_contact_email": "General",
    }
    res1 = client.post("/api/v1/auth/register", json=payload)
    assert res1.status_code == 201

    # Second registration with same email
    res2 = client.post("/api/v1/auth/register", json=payload)
    assert res2.status_code == 409
    assert "already exists" in res2.json()["detail"]


def test_admin_registration_rejected(client):
    payload = {
        "email": "admin@example.com",
        "password": "Password123!",
        "role": "admin",
        "full_name_or_company": "Admin User",
        "medical_license_or_contact_name": "ADM-001",
        "specialty_or_contact_email": "IT",
    }
    response = client.post("/api/v1/auth/register", json=payload)
    # Pydantic Literal validation rejects role="admin" with 422
    assert response.status_code == 422


def test_successful_login_and_token_response(client):
    reg_payload = {
        "email": "mfg.login@example.com",
        "password": "MfgPassword123!",
        "role": "manufacturer",
        "full_name_or_company": "BioHerbs Ltd",
        "medical_license_or_contact_name": "Alice Green",
        "specialty_or_contact_email": "alice@bioherbs.com",
    }
    res_reg = client.post("/api/v1/auth/register", json=reg_payload)
    assert res_reg.status_code == 201

    # Login
    login_payload = {
        "email": "mfg.login@example.com",
        "password": "MfgPassword123!",
    }
    res_login = client.post("/api/v1/auth/login", json=login_payload)
    assert res_login.status_code == 200
    token_data = res_login.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"
    assert token_data["role"] == "manufacturer"
    assert "password" not in token_data


def test_login_incorrect_password(client):
    reg_payload = {
        "email": "wrongpwd@example.com",
        "password": "RealPassword123!",
        "role": "doctor",
        "full_name_or_company": "Dr. Wrong",
        "medical_license_or_contact_name": "MED-554433",
        "specialty_or_contact_email": "Pediatrics",
    }
    client.post("/api/v1/auth/register", json=reg_payload)

    login_payload = {
        "email": "wrongpwd@example.com",
        "password": "WrongPassword999!",
    }
    res = client.post("/api/v1/auth/login", json=login_payload)
    assert res.status_code == 401
    assert "Invalid email or password" in res.json()["detail"]


def test_get_me_with_authenticated_jwt(client):
    reg_payload = {
        "email": "profile@example.com",
        "password": "Password123!",
        "role": "doctor",
        "full_name_or_company": "Dr. Profile",
        "medical_license_or_contact_name": "MED-776655",
        "specialty_or_contact_email": "Dermatology",
    }
    client.post("/api/v1/auth/register", json=reg_payload)

    # Login to get token
    login_res = client.post("/api/v1/auth/login", json={"email": "profile@example.com", "password": "Password123!"})
    token = login_res.json()["access_token"]

    # Access /api/v1/auth/me
    headers = {"Authorization": f"Bearer {token}"}
    me_res = client.get("/api/v1/auth/me", headers=headers)
    assert me_res.status_code == 200
    me_data = me_res.json()
    assert me_data["email"] == "profile@example.com"
    assert me_data["role"] == "doctor"
    assert me_data["status"] == "active"
    assert "password" not in me_data
    assert "hashed_password" not in me_data


def test_missing_and_invalid_token(client):
    # Missing token
    res1 = client.get("/api/v1/auth/me")
    assert res1.status_code == 401
    assert "Bearer token required" in res1.json()["detail"]

    # Malformed token
    res2 = client.get("/api/v1/auth/me", headers={"Authorization": "Bearer malformed.token.value"})
    assert res2.status_code == 401

    # Expired token
    from datetime import datetime, timezone
    expired_payload = {
        "sub": "some-id",
        "role": "doctor",
        "exp": int((datetime.now(timezone.utc) - timedelta(hours=1)).timestamp()),
    }
    expired_token = jwt.encode(expired_payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    res3 = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {expired_token}"})
    assert res3.status_code == 401
    assert "Token has expired" in res3.json()["detail"]


def test_role_based_access_authorization(client):
    from app.auth import create_access_token

    # Create doctor token and test doctor-only vs manufacturer/admin access
    doc_token = create_access_token(user_id="doc-123", role="doctor")
    doc_headers = {"Authorization": f"Bearer {doc_token}"}

    # Doctor trying to access admin dashboard summary -> 403 Forbidden
    res_admin = client.get("/api/v1/admin/dashboard/summary", headers=doc_headers)
    assert res_admin.status_code == 403
    assert "Insufficient permissions" in res_admin.json()["detail"]

    # Doctor trying to access manufacturer endpoint -> 403 Forbidden
    res_mfg = client.get("/api/v1/manufacturers/me/dashboard", headers=doc_headers)
    assert res_mfg.status_code == 403

    # Manufacturer token trying to access doctor certification endpoint -> 403 Forbidden
    mfg_token = create_access_token(user_id="mfg-123", role="manufacturer")
    mfg_headers = {"Authorization": f"Bearer {mfg_token}"}

    res_doc = client.get("/api/v1/doctors/me/verification", headers=mfg_headers)
    assert res_doc.status_code == 403
