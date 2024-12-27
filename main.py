'''Главная'''
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import DeclarativeBase, sessionmaker, relationship

def create():
    '''Вывод функции'''
    engine = create_engine("postgresql://postgres:12345678@localhost/lab9")
    class Base(DeclarativeBase):
        '''Класс'''
        pass

    class Users(Base):
        '''Класс'''
        __tablename__ = "Users"
        id = Column(Integer, primary_key=True, index=True)
        username = Column(String, unique=True)
        email = Column(String, unique=True)
        password = Column(String)
        posts = relationship("Posts", back_populates="user")

    class Posts(Base):
        '''Класс'''
        __tablename__ = "Posts"
        id = Column(Integer, primary_key=True, index=True)
        title = Column(String)
        content = Column(Text)
        user_id = Column(Integer, ForeignKey('Users.id'), nullable=False)
        user = relationship("Users", back_populates="posts")

    Base.metadata.create_all(bind=engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    user1 = Users(username = "sveta", email = "sveta@sveta", password = "sveta")
    user2 = Users(username = "anton", email = "anton@anton", password = "anton")
    user3 = Users(username = "anna", email = "anna@anna", password = "anna")

    session.add_all([user1, user2, user3])
    session.commit()

    post1 = Posts(title="Title 1 for user 1", content="Content 1 for user 1", user_id=user1.id)
    post2 = Posts(title="Title 2 for user 1", content="Content 2 for user 1", user_id=user1.id)
    post3 = Posts(title="Title 1 for user 2", content="Content 1 for user 2", user_id=user2.id)
    post4 = Posts(title="Title 2 for user 2", content="Content 2 for user 2", user_id=user2.id)
    post5 = Posts(title="Title 1 for user 3", content="Content 1 for user 3", user_id=user3.id)
    post6 = Posts(title="Title 2 for user 3", content="Content 2 for user 3", user_id=user3.id)

    session.add_all([post1, post2, post3, post4, post5, post6])
    session.commit()

    users = session.query(Users).all()
    for user in users:
        print(f"id: {user.id}, username: {user.username}, email: {user.email}, password: {user.password}")
    print()

    posts = session.query(Posts).join(Users).all()
    for post in posts:
        print(f"id: {post.id}, title: {post.title}, content: {post.content}, username: {post.user.username}")
    print()

    user_posts = session.query(Posts).join(Users).filter(Posts.user_id == user2.id).all()
    for post in user_posts:
        print(f"title: {post.title}, content: {post.content}")
    print()

    update_email = session.query(Users).filter(Users.id == 3).first()
    print(f"id: {update_email.id}, username: {update_email.username}, email: {update_email.email}, password:{update_email.password}")
    if update_email:
        update_email.email = "anna@mail.ru"
        session.commit()
    session.refresh(update_email)
    print(f"id: {update_email.id}, username: {update_email.username}, email: {update_email.email}, password:{update_email.password}")
    print()

    update_content = session.query(Posts).filter(Posts.id == 1).first()
    print(f"id: {update_content.id}, title: {update_content.title}, content: {update_content.content}, user_id: {update_content.user_id}")
    if update_content:
        update_content.content += " new content"
        session.commit()
    session.refresh(update_content)
    print(f"id: {update_content.id}, title: {update_content.title}, content: {update_content.content}, user_id: {update_content.user_id}")
    print()

    posts = session.query(Posts).join(Users).all()
    for post in posts:
        print(f"id: {post.id}, title: {post.title}, content: {post.content}, user_id: {post.user_id}, author: {post.user.username}")
    print()
    delete_post = session.query(Posts).filter(Posts.id == 8).first()
    if delete_post:
        session.delete(delete_post)
        session.commit()
    posts = session.query(Posts).join(Users).all()
    for post in posts:
        print(f"id: {post.id}, title: {post.title}, content: {post.content}, user_id: {post.user_id}, author: {post.user.username}")
    print()

    users = session.query(Users).all()
    for user in users:
        print(f"id: {user.id}, username: {user.username}, email: {user.email}, password: {user.password}")
    user_posts = session.query(Posts).filter(Posts.user_id == user1.id).all()
    for post in user_posts:
        print(f"title: {post.title}, content: {post.content}")
    print()
    delete_user = session.query(Users).filter(Users.id == 1).first()
    if delete_user:
        session.query(Posts).filter(Posts.user_id == delete_user.id).delete()
        session.delete(delete_user)
        session.commit()
    users = session.query(Users).all()
    for user in users:
        print(f"id: {user.id}, username: {user.username}, email: {user.email}, password: {user.password}")
    user_posts = session.query(Posts).filter(Posts.user_id == user1.id).all()
    for post in user_posts:
        print(f"title: {post.title}, content: {post.content}")
    print()

if __name__ == "__main__":
    create()
