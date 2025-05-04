from typing import Generic, TypeVar, Type, Any

from django.http import HttpRequest
from ninja import Query

from core.api.filters import PaginationIn, PaginationOut
from core.api.schemas import ApiResponse, ListPaginatedResponse

T = TypeVar('T') # тип схемы элемента списка
S = TypeVar('S') # тип сервисов
F = TypeVar('F') # тип фильтров

class BaseHandler(Generic[T, S, F]):
	'''
	Базовый обработчик
	'''
	schema: Type[T]
	filters: Type[F]
	service: Type[S]

	@classmethod
	def get_list_handler(
		cls,
		request: HttpRequest,
		filters: Query[F],
		pagination_in: Query[PaginationIn]
	) -> ApiResponse[ListPaginatedResponse[T]]:
		service = cls.service()
		entity_list = cls.service.get_list(
			filters=filters,
			pagination=pagination_in
		)
		entity_count = cls.service.get_count(
			filters=filters
		)
		items = [cls.schema.from_entity(obj) for obj in entity_list]
		pagination_out = PaginationOut(
					offset=pagination_in.offset,
					limit=pagination_in.limit,
					total=entity_count,
		)

		return ApiResponse(
		data=ListPaginatedResponse(items=items, pagination=pagination_out),
		)