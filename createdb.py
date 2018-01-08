from app import APP
from model import engine, Base

Base.metadata.create_all(engine)
