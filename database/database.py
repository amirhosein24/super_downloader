
from time import sleep
from threading import Thread
from datetime import datetime, date

from jdatetime import datetime as jdatetime
from dateutil.relativedelta import relativedelta
from sqlalchemy.pool import QueuePool
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float

from credentials.creds import Home, Bot, Admin

engine = create_engine(f"sqlite:///{Home}database/db.sqlite", poolclass=QueuePool, pool_recycle=1800,
                       connect_args={'check_same_thread': False})

Base = declarative_base()


class UserData(Base):
    __tablename__ = 'user_data'

    chat_id = Column(Integer, primary_key=True, unique=True)
    username = Column(String)
    firstname = Column(String)
    lastname = Column(String)
    usagenum = Column(Integer, default=0)
    usagesize = Column(Float, default=0)
    prem_till = Column(DateTime)
    timejoined = Column(DateTime)


Base.metadata.create_all(bind=engine)  # Create tables if not exist


###########################################################################################################################
def handle_prem_till(chat_id, add: int = 0):
    session = sessionmaker(bind=engine)()

    try:
        user_data = session.query(UserData).filter_by(chat_id=chat_id).first()

        if user_data:

            if add:
                if user_data.prem_till:
                    prem_till = user_data.prem_till + relativedelta(months=add)
                else:
                    prem_till = date.today() + relativedelta(months=add)

                user_data.prem_till = prem_till
                session.commit()

            if user_data.prem_till:
                iranian_date = jdatetime.fromgregorian(day=prem_till.day, month=prem_till.month, year=prem_till.year)
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
            timejoined=datetime.now()
        )
        session.add(new_user)
        session.commit()
        session.close()
        return True

    except:
        session.rollback()
        session.close()
        return False


###########################################################################################################################
def usage_num(chat_id: int, add: bool = False):
    session = sessionmaker(bind=engine)()
    user_data = session.query(UserData).filter_by(chat_id=chat_id).first()

    if user_data:
        if add:
            user_data.usagenum += 1
            session.commit()

        usage = user_data.usagenum
        session.close()
        return usage

    else:
        session.close()
        return False


###########################################################################################################################
def usage_size(chat_id, amount: float = 0):
    session = sessionmaker(bind=engine)()
    user_data = session.query(UserData).filter_by(chat_id=chat_id).first()

    if user_data:
        if amount:
            user_data.usagesize += amount
            session.commit()

        entire_size = round(user_data.usagesize, 2)
        session.close()
        return entire_size

    else:
        session.close()
        return False


###########################################################################################################################
def check_prem_till_daily():
    while True:
        session = sessionmaker(bind=engine)()

        try:
            user_data = session.query(UserData).filter(UserData.prem_till != None).all()

            for user in user_data:
                if user.prem_till < datetime.now():
                    user.prem_till = None
                    try:
                        Bot.send_message(user.chat_id, f"premuim is over")
                    except:
                        pass

            session.commit()

        except Exception as error:
            Bot.send_message(Admin, f"error in database.check_prem_till_daily, error in line {error.__traceback__.tb_lineno}:\n{error}")
            session.rollback()

        finally:
            session.close()

        if user_data:
            del user_data

        now = datetime.now()
        delta = now.replace(hour=23, minute=59, second=59) - now
        sleep(abs(delta.total_seconds()))


Thread(target=check_prem_till_daily).start()
