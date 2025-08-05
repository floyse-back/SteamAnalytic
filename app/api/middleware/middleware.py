import time
from typing import Callable, Awaitable
import logging
from fastapi import Request,Response

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                    )

async def log_middleware(request:Request,call_next:Callable[[Request],Awaitable[Response]]):
    logger.info(f"Method: %s Path %s",request.method,request.url.path)
    start_time = time.process_time()
    response = await call_next(request)
    process_time = time.process_time() - start_time
    logger.info("Status code: %s Processed in %.2f sec", response.status_code, process_time)

    return response
