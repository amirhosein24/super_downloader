from os import getcwd
from datetime import datetime

from sqlalchemy.pool import QueuePool
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from sqlalchemy import create_engine, Column, Integer, String, DateTime


engine = create_engine(f"sqlite:///{getcwd()}/db.sqlite", poolclass=QueuePool, pool_recycle=1800,
                       connect_args={'check_same_thread': False})

Base = declarative_base()

class UserData(Base):
    __tablename__ = 'user_data'

    chat_id = Column(Integer, primary_key=True)
    username = Column(String)
    firstname = Column(String)
    lastname = Column(String)
    timejoined = Column(DateTime)
    usageNum = Column(Integer)
    usageSize = Column(Integer)

Base.metadata.create_all(bind=engine)  # Create tables if not exist




# function to add user 
def add_user(chat_id, username, firstname, lastname):
    session = sessionmaker(bind=engine)()

    try:
        new_user = UserData(
            chat_id=chat_id,
            username=username,
            firstname=firstname,
            lastname=lastname,
            timejoined=datetime.now(),
            usageNum = 0,
            usageSize = 0
        )

        session.add(new_user)
        session.commit()
        session.close()
        return True
    except :
        session.rollback()
        session.close()
        return False


# add_user(2152, "@!$%", "erger", "Qrtqrt")

def AddUsageNum(chat_id):
    Session = sessionmaker(bind=engine)
    session = Session()

    user_data = session.query(UserData).filter_by(chat_id=chat_id).first()


    if user_data:

        user_data.usageNum += 1
        session.commit()
        session.close()
        return True

    else:
        # Handle the case where user_data is None (user not found)
        session.close()
        return False
    
