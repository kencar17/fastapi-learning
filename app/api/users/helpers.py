from sqlmodel import select

from app.api.users.models.user import User


def get_user_by_username(*, session, username: str) -> User | None:
    statement = select(User).where(User.username == username)
    session_user = session.exec(statement).first()
    return session_user
