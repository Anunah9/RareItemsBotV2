import asyncio
import logging

logging.basicConfig(
    filename="log.log",
    level=logging.ERROR,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('logger')
