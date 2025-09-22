from fastapi.responses import Response

from json import dumps
from typing import Any, Dict


def generate_api_answer(
        status_code: int, 
        **kwargs: Any
    ) -> Dict[str, Any]:
    """
    Форматтер стандантизированных ответов API для успешных запросов
    """
    data = {
        "success": True, 
        **kwargs
    }
    return Response(
        content=dumps(data),
        status_code=status_code
    )

