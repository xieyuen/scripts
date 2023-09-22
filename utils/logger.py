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


trace = logger.trace
debug = logger.debug
info = logger.info
success = logger.success
warning = warn = logger.warning
error = logger.error
critical = crit = logger.critical
catch = logger.catch
exception = logger.exception
