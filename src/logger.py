import logging

LOG_FILENAME = 'paranoico.log'
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'

logging.basicConfig(filename=LOG_FILENAME,
                    filemode='w',
                    format=LOG_FORMAT,
                    level=logging.WARNING)

logger = logging.getLogger('logger')
