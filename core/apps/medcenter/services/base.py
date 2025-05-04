from abc import (
    ABC,
    abstractmethod,
)
from collections.abc import Iterable
from typing import (
    Generic,
    TypeVar,
)

from django.db.models import Q

from core.api.filters import PaginationIn


F = TypeVar("F")  # тип фильтров
E = TypeVar("E")  # тип сущностей
DTO = TypeVar("DTO")


class BaseService(ABC, Generic[F, E, DTO]):
    filters: type[F]
    entity: type[E]
    model: type[DTO]

    @classmethod
    def get_list(
        cls,
        filters: type[F],
        pagination: PaginationIn,
    ) -> Iterable[E]:
        query = cls._build_query(filters=filters)
        qs = cls.model.objects.filter(query)[
            pagination.offset : pagination.offset + pagination.limit  # noqa
        ]

        return [dto.to_entity() for dto in qs]

    @classmethod
    def get_count(cls, filters: type[F]) -> int:
        query = cls._build_query(filters=filters)

        return cls.model.objects.filter(query).count()

    @classmethod
    @abstractmethod
    def _build_query(cls, filters: type[F]) -> Q: ...
