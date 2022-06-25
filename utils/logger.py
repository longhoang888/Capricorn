
import logging
from logging import config


class Log:

    """Private variables"""

    __logger = None  # The actual Logger

    __instance = None  # Singleton Object

    # Default error log file name
    __error_log = "{}error.log".format("logs/")

    # Default log message format
    __logformat = "%(asctime)s : %(levelname)s : %(module)s : %(funcName)s : %(lineno)d : (Process Details : (%(process)d, %(processName)s), Thread Details : (%(thread)d, %(threadName)s))\nLog Message : %(message)s"

    # Default date time format
    __datefmt = '%m/%d/%Y %I:%M:%S %p'

# <FUNCTION START>-------------------------------------------------------------------------------------------
    @staticmethod
    def active(writer="main"):
        """Static factory method return an instance of Log"""
        if Log.__instance == None:
            Log(writer)
        return Log.__instance
# <FUNCTION END>---------------------------------------------------------------------------------------------

# <FUNCTION START>-------------------------------------------------------------------------------------------
    def __init__(self, writer):
        """Prive constructor method for Log"""
        if Log.__instance == None:
            Log.__instance = self
            # Read configuration in log.conf file
            try:
                config.fileConfig('log.conf')
                Log.__logger = logging.getLogger(writer)
            except Exception as e:
                Log.__logger = logging.getLogger(writer)
                self.__logger.setLevel(logging.DEBUG)
                error_log = logging.FileHandler(self.__error_log)
                error_log.setLevel(logging.ERROR)
                formatter = logging.Formatter(
                    self.__logformat, datefmt=self.__datefmt)
                error_log.setFormatter(formatter)
                self.__logger.addHandler(error_log)
                self.__logger.error("Error Type : {}, Error Message : {}".format(
                    type(e).__name__, e))
# <FUNCTION END>---------------------------------------------------------------------------------------------

# <FUNCTION START>-------------------------------------------------------------------------------------------

    def write(self, e):
        """ 
        Write log to error_log file

        Input: Exception

        """
        self.__logger.error(
            "Error Type : {}, Error Message : {}".format(type(e).__name__, e))
# <FUNCTION END>---------------------------------------------------------------------------------------------
