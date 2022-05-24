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

from abc import ABC, abstractmethod
from typing import Any, List

""" START of design pattern 1: Strategy """
class Context():
    def __init__(self, strategy: Strategy) -> None:
        self._strategy = strategy

    @property
    def strategy(self) -> Strategy:
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: Strategy) -> None:
        self._strategy = strategy

    def sortAccordingToStrategy(self, data: List) -> List:
        result = self._strategy.sortList(data)
        return result


class Strategy(ABC):
    @abstractmethod
    def sortList(self, data: List):
        pass

    def compareRatings(self, movie):
        return movie.get("rating")

class ConcreteStrategyDescending(Strategy):
    def sortList(self, data: List) -> List:
        return sorted(data, key=super().compareRatings, reverse=True)

class ConcreteStrategyAscending(Strategy):
    def sortList(self, data: List) -> List:
        return sorted(data, key=super().compareRatings)
""" END of design pattern 1: Strategy """


""" START of design pattern 2: Builder """
class Builder(ABC):
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


class ConcreteBuilder(Builder):
    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self._user = user()

    @property
    def user(self) -> user:
        user = self._user
        self.reset()
        return user

    def add_password(self, password) -> None:
        self._user.add(password)

    def add_email(self, email) -> None:
        self._user.add(email)

    def add_pref_key(self, interestList: List) -> None:
        preference_key = str((int(interestList[0]) + int(interestList[1]) + int(interestList[2])) % 4 + 1)
        self._user.add(preference_key)


class user():
    def __init__(self) -> None:
        self.parts = []

    def add(self, part: Any) -> None:
        self.parts.append(part)

class Director:
    def __init__(self) -> None:
        self._builder = None

    @property
    def builder(self) -> Builder:
        return self._builder

    @builder.setter
    def builder(self, builder: Builder) -> None:
        self._builder = builder

    def buildUser(self, email, password, interestList) -> None:
        self.builder.add_password(password)
        self.builder.add_email(email)
        self.builder.add_pref_key(interestList)
""" END of design pattern 2: Builder """


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