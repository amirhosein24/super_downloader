
from time import sleep
from threading import Thread
from datetime import datetime, date

from jdatetime import datetime as jdatetime
from dateutil.relativedelta import relativedelta

from credentials.creds import Home

from datetime import datetime, timedelta

from sqlalchemy.pool import QueuePool
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, DateTime

engine = create_engine(f"sqlite:///{Home}database/db.sqlite", poolclass=QueuePool,
                       pool_recycle=1800, connect_args={'check_same_thread': False})

Base = declarative_base()


class UserData(Base):
    __tablename__ = 'user_data'

    id = Column(Integer, autoincrement=True)
    chat_id = Column(Integer, primary_key=True)
    username = Column(String)
    firstname = Column(String)
    lastname = Column(String)
    usagenum = Column(Integer, default=0)
    usagesize = Column(Integer, default=0)
    prem_till = Column(DateTime)
    timejoined = Column(DateTime)


Base.metadata.create_all(bind=engine)  # Create tables if not exist


############################################################################################################################################


def handle_prem_till(chat_id, add: bool = False):
    session = sessionmaker(bind=engine)()

    try:
        user_data = session.query(UserData).filter_by(chat_id=chat_id).first()

        if user_data:

            if add:
                if user_data.prem_till:
                    prem_till = user_data.prem_till + relativedelta(months=1)
                else:
                    prem_till = date.today() + relativedelta(months=1)

                user_data.prem_till = prem_till
                session.commit()
                iranian_date = jdatetime.fromgregorian(
                    day=prem_till.day, month=prem_till.month, year=prem_till.year)

                return iranian_date.strftime("%Y/%m/%d")

            prem_till = user_data.prem_till
            if prem_till:
                iranian_date = jdatetime.fromgregorian(
                    day=prem_till.day, month=prem_till.month, year=prem_till.year)

                return iranian_date.strftime("%Y/%m/%d")
            else:
                return False

        else:
            return False

    finally:
        session.close()


###########################################################################################################################
def add_user(chat_id, username, firstname, lastname):
    session = sessionmaker(bind=engine)()
    try:
        new_user = UserData(
            chat_id=chat_id,
            username=username,
            firstname=firstname,
            lastname=lastname,
            timejoined=datetime.now())
        session.add(new_user)
        session.commit()
        session.close()
        return True
    except:
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


def check_prem_till():
    while True:
        session = sessionmaker(bind=engine)()

        try:
            user_data = session.query(UserData).all()
            for user in user_data:
                if user.prem_till:
                    if user.prem_till < datetime.now():
                        user.prem_till = None
            session.commit()

        except:
            session.rollback()

        finally:
            session.close()

        now = datetime.now()
        next_time = now.replace(hour=23, minute=59, second=59)
        delta = next_time - now

        sleep(abs(delta.total_seconds()))


Thread(target=check_prem_till).start()
