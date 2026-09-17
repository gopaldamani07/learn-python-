import logging


# ---- 1. Configure the logger ----
logger = logging.getLogger("my_app")
logger.setLevel(logging.DEBUG)          # lowest level this logger will handle

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Console handler -> only INFO and above
console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(formatter)

# File handler -> everything, appended to app.log
file_handler = logging.FileHandler("app.log")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(console)
logger.addHandler(file_handler)


# ---- 2. Use it ----
def divide(a, b):
    logger.debug("divide() called with a=%s b=%s", a, b)
    try:
        result = a / b
    except ZeroDivisionError:
        logger.exception("Cannot divide %s by zero", a)   # logs ERROR + traceback
        return None
    logger.info("Result: %s / %s = %s", a, b, result)
    return result


if __name__ == "__main__":
    logger.debug("This is DEBUG  - file only")
    logger.info("This is INFO   - console + file")
    logger.warning("This is WARNING")
    logger.error("This is ERROR")
    logger.critical("This is CRITICAL")

    divide(10, 2)
    divide(5, 0)
