import logging

def setup_logger(name: str):

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    return logger


# Example usage:
    #from src.utils.logger import setup_logger
    # logger = setup_logger(__name__)
    # logger.info("Starting rainfall extraction")