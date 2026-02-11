"""
Wait for Load Balancer to be ready before starting traffic generation
"""

import asyncio
import aiohttp
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def wait_for_load_balancer(url: str = "http://load-balancer:8000", max_attempts: int = 30):
    """Wait for load balancer to be ready"""
    for attempt in range(max_attempts):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{url}/health", timeout=aiohttp.ClientTimeout(total=5)) as response:
                    if response.status == 200:
                        logger.info("Load balancer is ready!")
                        return True
        except Exception as e:
            logger.info(f"Attempt {attempt + 1}/{max_attempts}: Load balancer not ready yet ({e})")
            await asyncio.sleep(2)
    
    logger.error("Load balancer did not become ready in time")
    return False

if __name__ == "__main__":
    asyncio.run(wait_for_load_balancer())
