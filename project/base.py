"""File to import to create SQL-Alchemy linked ORM Classes.
Derive from Base
E.g. class Clip(Base):
         __table__="CLIPS"
         ...

Use Session to manipulate database, FROM INSIDE CLASSES ONLY (Mostly)
session = Session()
session.query(id=...)
try:
    session.add(new_class)
    session.commit()
except:
    raise #idk if session.close() gets called if this happens?
finally:
    session.close()

For routes.py, public-facing stuff, you should be using the functions in database.py
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine('sqlite:///clipbucket.db')
#Class defined to derive database objects from:
Base=declarative_base()
#Class defined to create sessions later on
Session = sessionmaker(bind=engine)
