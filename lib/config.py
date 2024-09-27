import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(processName)s - %(threadName)s - %(filename)s - %(funcName)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)