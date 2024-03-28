# logging_config.py
import logging

def setup_logging():
    logging.basicConfig(
        filename='application.log',  # Saves logs to a file
        level=logging.INFO,  # Sets the minimum severity level to capture
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Custom format for log messages
        datefmt='%Y-%m-%d %H:%M:%S',  # Date/time format
    )

    # Configures an additional handler for console output with WARNING level or higher
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(logging.Formatter('%(name)s - %(levelname)s - %(message)s'))
    logging.getLogger('').addHandler(console_handler)
