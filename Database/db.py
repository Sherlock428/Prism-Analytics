from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = "sqlite:///database.db"

engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    """cria uma sessão com o banco de dados"""
    with Session(engine) as session:
        yield session

def init_db():
    """Cria as tabelas do banco"""
    SQLModel.metadata.create_all(engine)