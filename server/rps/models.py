from sqlalchemy import create_engine, Column, Integer, String, DateTime, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import dotenv_values

# Postgres database
config = dotenv_values(".env")  # Contains the database strings
db_conn_url = f"postgresql+psycopg2://{config['DB_USER']}:{config['DB_PASS']}@{config['DB_URL']}:{config['DB_PORT']}/{config['DB_NAME']}"
engine = create_engine(db_conn_url)

Base = declarative_base()

Session = sessionmaker(bind=engine)
db = Session()


class GameResult(Base):
    __tablename__ = "gameresults"

    id = Column(Integer, primary_key=True)
    player1_choice = Column(String)
    player2_choice = Column(String)
    result = Column(String)
    timestamp = Column(DateTime, server_default=func.now())

    def __init__(self, player1_choice, player2_choice, result):
        self.player1_choice = player1_choice
        self.player2_choice = player2_choice
        self.result = result


Base.metadata.create_all(engine)
