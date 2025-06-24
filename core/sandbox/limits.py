import resource
import logging

logger = logging.getLogger("ResourceLimiter")
logging.basicConfig(level=logging.INFO)

def set_limits(cpu_seconds=2, max_memory_mb=100):
    try:
        # Limit CPU time
        resource.setrlimit(resource.RLIMIT_CPU, (cpu_seconds, cpu_seconds))
        logger.info(f"[Limiter] CPU limit set to {cpu_seconds} seconds")

        # Limit virtual memory
        max_memory = max_memory_mb * 1024 * 1024
        resource.setrlimit(resource.RLIMIT_AS, (max_memory, max_memory))
        logger.info(f"[Limiter] Memory limit set to {max_memory_mb} MB")
        
    except ValueError as ve:
        logger.error(f"[Limiter] ValueError: {ve}")
    except resource.error as re:
        logger.error(f"[Limiter] ResourceError: {re}")
