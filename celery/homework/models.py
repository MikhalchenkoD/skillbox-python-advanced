from flask import jsonify
from sqlalchemy import Column, Integer, String, create_engine, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine('sqlite:///celery.db')
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    is_subscribed = Column(Boolean, default=False)

    @classmethod
    def set_user_subscribed(cls, email):
        user = session.query(User).filter(User.email == email).first()

        if not user:
            user = User(email=email)
            session.add(user)
            session.commit()

        user.is_subscribed = True

        session.commit()
        session.close()

        return 'OK'

    @classmethod
    def set_user_unsubscribed(cls, email):
        user = session.query(User).filter(User.email == email).first()
        user.is_subscribed = False
        session.commit()
        session.close()

        return 'OK'

    @classmethod
    def get_subscribed_users(cls):
        users = session.query(User).filter(User.is_subscribed == True).all()
        # users_data = [{"id": user.id, "email": user.email, "is_subscribed": user.is_subscribed} for user in
        #               users]
        session.close()
        return users


Base.metadata.create_all(engine)


