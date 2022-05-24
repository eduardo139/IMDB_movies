""" Stuff I added """
from __future__ import annotations
""" END Stuff I added """

import os
from sqlalchemy import (
    MetaData,
    Column,
    Integer,
    String,
    Float,
    TIMESTAMP,
    Text,
    create_engine
)
from sqlalchemy.ext.declarative import declarative_base

""" Stuff I added """

from abc import ABC, abstractmethod
from typing import Any


class Builder(ABC):
    """
    The Builder interface specifies methods for creating the different parts of
    the user objects.
    """

    @property
    @abstractmethod
    def user(self) -> None:
        pass

    @abstractmethod
    def add_password(self, password) -> None:
        pass

    @abstractmethod
    def add_email(self, email) -> None:
        pass

    @abstractmethod
    def add_pref_key(self, pref_key) -> None:
        pass


class ConcreteBuilder1(Builder):
    """
    The Concrete Builder classes follow the Builder interface and provide
    specific implementations of the building steps. Your program may have
    several variations of Builders, implemented differently.
    """

    def __init__(self) -> None:
        """
        A fresh builder instance should contain a blank user object, which is
        used in further assembly.
        """
        self.reset()

    def reset(self) -> None:
        self._user = user()

    @property
    def user(self) -> user:
        """
        Concrete Builders are supposed to provide their own methods for
        retrieving results. That's because various types of builders may create
        entirely different users that don't follow the same interface.
        Therefore, such methods cannot be declared in the base Builder interface
        (at least in a statically typed programming language).

        Usually, after returning the end result to the client, a builder
        instance is expected to be ready to start producing another user.
        That's why it's a usual practice to call the reset method at the end of
        the `getuser` method body. However, this behavior is not mandatory,
        and you can make your builders wait for an explicit reset call from the
        client code before disposing of the previous result.
        """
        user = self._user
        self.reset()
        return user

    def add_password(self, password) -> None:
        self._user.add(password)

    def add_email(self, email) -> None:
        self._user.add(email)

    def add_pref_key(self, pref_key) -> None:
        self._user.add(pref_key)


class user():
    """
    It makes sense to use the Builder pattern only when your users are quite
    complex and require extensive configuration.

    Unlike in other creational patterns, different concrete builders can produce
    unrelated users. In other words, results of various builders may not
    always follow the same interface.
    """

    def __init__(self) -> None:
        self.parts = []

    def add(self, part: Any) -> None:
        self.parts.append(part)

    def list_parts(self) -> None:
        print(f"user parts: {', '.join(self.parts)}", end="")


class Director:
    """
    The Director is only responsible for executing the building steps in a
    particular sequence. It is helpful when producing users according to a
    specific order or configuration. Strictly speaking, the Director class is
    optional, since the client can control builders directly.
    """

    def __init__(self) -> None:
        self._builder = None

    @property
    def builder(self) -> Builder:
        return self._builder

    @builder.setter
    def builder(self, builder: Builder) -> None:
        """
        The Director works with any builder instance that the client code passes
        to it. This way, the client code may alter the final type of the newly
        assembled user.
        """
        self._builder = builder

    """
    The Director can construct several user variations using the same
    building steps.
    """

    def build_full_featured_user(self) -> None:
        self.builder.add_password("pass1")
        self.builder.add_email("here@this.com")
        self.builder.add_pref_key("1")
""" END Stuff I added"""


def get_postgres_uri():
    host = os.environ.get("DB_HOST", "postgres")
    port = 5432
    password = os.environ.get("DB_PASS", "abc123")
    user, db_name = "movies", "movies"
    return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"


Base = declarative_base(
    metadata=MetaData(),
)


engine = create_engine(
    get_postgres_uri(),
    isolation_level="REPEATABLE READ",
)


class Movie(Base):
    __tablename__ = "movies"

    movie_id = Column(Integer, primary_key=True)
    preference_key = Column(Integer)
    movie_title = Column(String)
    rating = Column(Float)
    year = Column(Integer)
    create_time = Column(TIMESTAMP(timezone=True), index=True)


def start_mappers():
    Base.metadata.create_all(engine)