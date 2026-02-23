import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.main import create_app
from app.db.session import Base, get_db


# Test database URL
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test_db.sqlite"


@pytest_asyncio.fixture
async def test_db():
    """Create test database."""
    engine = create_async_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    AsyncSessionLocal = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    
    async with AsyncSessionLocal() as session:
        yield session
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def client(test_db):
    """Create test client."""
    app = create_app()
    
    async def override_get_db():
        yield test_db
    
    app.dependency_overrides[get_db] = override_get_db
    
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_root(client):
    """Test root endpoint."""
    response = await client.get("/")
    assert response.status_code == 200
    assert "Mental Math Trainer" in response.json()["message"]


@pytest.mark.asyncio
async def test_health(client):
    """Test health endpoint."""
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


@pytest.mark.asyncio
async def test_get_levels(client):
    """Test get levels endpoint."""
    response = await client.get("/api/v1/tasks/levels")
    assert response.status_code == 200
    data = response.json()
    assert "levels" in data
    assert len(data["levels"]) == 10


@pytest.mark.asyncio
async def test_register_and_login(client):
    """Test registration and login."""
    # Register
    response = await client.post("/api/v1/auth/register")
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    
    # Get user info
    token = data["access_token"]
    response = await client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
