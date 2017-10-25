import os
import logging
from datetime import datetime


def setup_logging(config_name):
    """
    Sets up logging to console (INFO+) and logging of log file
    logs/myapp-<timestamp>.log. You can create a an extra logger to represent
    areas in your app: logger1 = logging.getLogger('area1')

    Logging Levels:

    https://docs.python.org/3/howto/logging.html#logging-levels

    DEBUG (default for FILE): Detailed information, typically of interest only
        when diagnosing problems.
    INFO (default for CONSOLE): Confirmation that things are working as
        expected.
    WARNING: An indication that something unexpected happened, or indicative of
        some problem in the near future (e.g. 'disk space low').
        The software is still working as expected.
    ERROR: Due to a more serious problem, the software has not been able
        to perform some function.
    CRITICAL: A serious error, indicating that the program itself may be unable
        to continue running.

    Params
        config_name
    """

    # Make sure the logs folder exists (avoid FileNotFoundError)
    if not os.path.isdir('logs'):
        os.makedirs('logs')

    # Set the logging levels
    log_lvl_file = 'DEBUG'
    log_lvl_console = 'INFO'

    if config_name == 'development':
        log_lvl_console = 'DEBUG'
    elif config_name == 'production':
        log_lvl_file = 'INFO'

    # Set up logging to a file (overwriting)
    log_filename = ('logs/myapp-{}.log'.format(datetime.utcnow().strftime(
        "%Y%m%d")))
    # Possibly use %(pathname)s:%(lineno)d
    logging.basicConfig(format='%(asctime)s.%(msecs)03d - %(name)-12s - '
                               '%(levelname)-8s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename=log_filename,
                        filemode='w',
                        level=log_lvl_file)

    # Create a handler that writes INFO messages or higher to sys.stderr
    console = logging.StreamHandler()
    console.setLevel(log_lvl_console)

    # Create a formatter without timestamp for the console handler
    console_formatter = logging.Formatter(
        '%(name)-12s - %(levelname)-8s - %(message)s')

    # Add formatter to console handler
    console.setFormatter(console_formatter)

    # Add console handler to root logger
    logging.getLogger('').addHandler(console)

    # Demo usage
    # logger = logging.getLogger('setup_logging')
    # logger.debug('a debug log message')
    # logger.info('an info log message')
    # logger.warning('a warning log message')
    # logger.error('an error log message')
    # logger.critical('a critical log message')
