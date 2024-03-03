from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()


class Usuario(Base):
    __tablename__ = "user_account"
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    nome_completo = Column(String)

    endereco = relationship("Endereco", back_populates="usuario", cascade="all, delete-orphan")

    def __repr__(self):
        return f"Usuario(id={self.id}, nome={self.nome}, nome_completo={self.nome_completo})"


class Endereco(Base):
    __tablename__ = "address"
    id = Column(Integer, primary_key=True)
    endereco_email = Column(String(30), nullable=False)
    usuario_id = Column(Integer, ForeignKey("user_account.id"), nullable=False)

    usuario = relationship("Usuario", back_populates="endereco")

    def __repr__(self):
        return f"Endereco(id={self.id}, endereco_email={self.endereco_email})"


def create_engine_and_session():
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return engine, Session


def insert_users_data(session):
    users_data = [
        {"nome": "valdemar", "nome_completo": "Valdemar Teider", "enderecos": ["valdemar@example.com"]},
        {"nome": "joao", "nome_completo": "João Teider", "enderecos": ["joao@example.com", "joao2@example.com"]},
        {"nome": "dani", "nome_completo": "Dani Teider", "enderecos": []}
    ]

    for user_info in users_data:
        user = Usuario(nome=user_info["nome"], nome_completo=user_info["nome_completo"])
        user.endereco = [Endereco(endereco_email=email) for email in user_info["enderecos"]]
        session.add(user)

    session.commit()


def main():
    engine, Session = create_engine_and_session()
    session = Session()

    try:
        insert_users_data(session)

        # Restante do código permanece o mesmo

    except Exception as e:
        print(f"Falha: {e}")
        session.rollback()

    finally:
        session.close()


if __name__ == "__main__":
    main()

