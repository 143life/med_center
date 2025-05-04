from abc import ABC, abstractclassmethod, abstractmethod
from collections.abc import Iterable
from typing import Generic, TypeVar, Type

from django.db.models import Q

from ninja import Query

from core.api.filters import PaginationIn

F = TypeVar('F') # тип фильтров
E = TypeVar('E') # тип сущностей
DTO = TypeVar('DTO')

class BaseService(ABC, Generic[F, E, DTO]):
	filters: Type[F]
	entity: Type[E]
	model: Type[DTO]

	@classmethod
	def get_list(
			cls,
			filters: Type[F],
			pagination: PaginationIn,
	) -> Iterable[E]:
			query = cls._build_query(filters=filters)
			qs = cls.model.objects.filter(query)[
					pagination.offset : pagination.offset + pagination.limit # noqa
			]

			return [dto.to_entity() for dto in qs]

	@classmethod
	def get_count(cls, filters: Type[F]) -> int:
			query = cls._build_query(filters=filters)

			return cls.model.objects.filter(query).count()
	
	@classmethod
	@abstractmethod
	def _build_query(cls, filters: Type[F]) -> Q: ...