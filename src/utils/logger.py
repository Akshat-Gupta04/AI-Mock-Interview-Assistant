import logging
import os

def setup_logger(name="app_logger", log_file="app.log", level=logging.INFO):
    """
    Sets up a logger for the application.

    Args:
        name (str): Name of the logger.
        log_file (str): File to log messages.
        level (int): Logging level.

    Returns:
        logging.Logger: Configured logger instance.
    """

    logger = logging.getLogger(name)
    logger.setLevel(level)

   
    if not logger.handlers:
    
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)


        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger

default_logger = setup_logger()

def get_logger(name="app_logger"):
    """
    Get the logger instance.

    Args:
        name (str): Name of the logger.

    Returns:
        logging.Logger: Logger instance.
    """
    return logging.getLogger(name)