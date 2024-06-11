
from datetime import datetime, timedelta

from sqlalchemy.pool import QueuePool
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, DateTime

engine = create_engine(f"sqlite:///{__file__[:-11]}db.sqlite", poolclass=QueuePool, pool_recycle=1800, connect_args={'check_same_thread': False})

Base = declarative_base()

class UserData(Base):
    __tablename__ = 'user_data'

    id = Column(Integer, autoincrement=True)
    chat_id = Column(Integer, primary_key=True)
    username = Column(String)
    firstname = Column(String)
    lastname = Column(String)
    timejoined = Column(DateTime)
    usageNum = Column(Integer)
    usageSize = Column(Integer)
    prem = Column(DateTime)

Base.metadata.create_all(bind=engine)  # Create tables if not exist



########################################################################################################################### 
def is_prem(chat_id):
    session = sessionmaker(bind=engine)()
    user_data = session.query(UserData).filter_by(chat_id=chat_id).first()
    if user_data:
        till = user_data.prem
        session.close()
        if till:
            now = datetime.strptime(datetime.now().strftime('%Y/%m/%d'), '%Y/%m/%d')
            if now <= till:
                return True
            elif now > till:
                return False
        return False
    else:
        return False

############################################################################################################################################
def add_prem(chat_id, month):
    session = sessionmaker(bind=engine)()
    if is_prem(chat_id):
        user_data = session.query(UserData).filter_by(chat_id=chat_id).first()
        future_date = user_data.prem + timedelta(days=month*31)
        user_data.prem = future_date
        session.commit()
        session.close()
        return True
    else:
        user_data = session.query(UserData).filter_by(chat_id=chat_id).first()
        if user_data:
            current_date = datetime.now().date()
            future_date = current_date + timedelta(days=month*31)
            user_data.prem = future_date
            session.commit()
            session.close()
            return True
        session.close()
        return False


########################################################################################################################### 
def add_user(chat_id, username, firstname, lastname):
    session = sessionmaker(bind=engine)()
    try:
        new_user = UserData(
            chat_id=chat_id,
            username=username,
            firstname=firstname,
            lastname=lastname,
            timejoined=datetime.now(),
            usageNum=0)
        session.add(new_user)
        session.commit()
        session.close()
        return True
    except :
        session.rollback()
        session.close()
        return False

###################################################################################################################### 
def AddUsageNum(chat_id):
    session = sessionmaker(bind=engine)()
    user_data = session.query(UserData).filter_by(chat_id=chat_id).first()
    if user_data:
        user_data.usageNum += 1
        session.commit()
        session.close()
        return True
    else:
        session.close()
        return False