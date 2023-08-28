from loguru import logger


logger.remove()
logger.add(
    "logs/latest.log",
    format="[{time:YYYY-MM-DD HH:mm:ss}] [{level}] | {message}",
    level="DEBUG",
    rotation="1 week",
    retention="100 days",
    encoding="utf-8",
)


def trace(msg): logger.trace(msg)
def debug(msg): logger.debug(msg)
def info(msg): logger.info(msg)
def success(msg): logger.success(msg)
def warning(msg): logger.warning(msg)
def warn(msg): logger.warning(msg)
def error(msg): logger.error(msg)
def critical(msg): logger.critical(msg)
def crit(msg): logger.critical(msg)
