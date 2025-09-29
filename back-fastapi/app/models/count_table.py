# Ce fichier a été modifié pour utiliser 
# les fonctionnalités de SQLAlchemy de manière plus appropriée.

from sqlalchemy import Column, Integer
from ..database import Base

class CountTable(Base):
    __tablename__ = 'count_table'

    id = Column(Integer, primary_key=True, autoincrement=True)
    count_number = Column(Integer, nullable=False, default=0)