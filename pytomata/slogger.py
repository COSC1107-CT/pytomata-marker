"""This is a logger that supports indentation by depth, color coding, and custom time zones.

Sebastian Sardina @ 2025 - ssardina@gmail.com

"""
from datetime import datetime
import logging
import time
from colorlog import ColoredFormatter
from zoneinfo import ZoneInfo

MELBOURNE_TZ = ZoneInfo("Australia/Melbourne")
UTC = ZoneInfo("UTC")

LOG_LEVEL = logging.INFO
LOGGING_FMT = "  %(log_color)s%(asctime)s - %(name)s - %(levelname)-6s%(reset)s | %(log_color)s%(message)s%(reset)s"
LOGGING_DATE = "%Y-%m-%d %H:%M:%S"


class IndentLogger(logging.getLoggerClass()):
    """This improves the logger by adding a depth parameter.
    Such parameter can then be used by the formatter to indent the message."""
    def _log(
        self,
        level,
        msg,
        args,
        exc_info=None,
        extra=None,
        stack_info=False,
        stacklevel=1,
        depth=0,
    ):
        if extra is None:
            extra = {}
        extra["depth"] = depth
        super()._log(level, msg, args, exc_info, extra, stack_info, stacklevel)

    def debug(self, msg, *args, depth=0, **kwargs):
        self._log(logging.DEBUG, msg, args, depth=depth, **kwargs)

    def info(self, msg, *args, depth=0, **kwargs):
        self._log(logging.INFO, msg, args, depth=depth, **kwargs)

    def warning(self, msg, *args, depth=0, **kwargs):
        self._log(logging.WARNING, msg, args, depth=depth, **kwargs)

    def error(self, msg, *args, depth=0, **kwargs):
        self._log(logging.ERROR, msg, args, depth=depth, **kwargs)

    def critical(self, msg, *args, depth=0, **kwargs):
        self._log(logging.CRITICAL, msg, args, depth=depth, **kwargs)


class IndentColorFormatter(ColoredFormatter):
    """This formatter adds indentation to the message based on the depth parameter. It also a colored formatter and allows setting a timezone for reporting dates and times."""
    def __init__(self, *args, timezone=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.timezone = timezone

    def format(self, record):
        depth = getattr(record, "depth", 0)
        indent = "\t" * depth
        record.msg = f"{indent}{record.getMessage()}"  # Add indent
        return super().format(record)

    def formatTime(self, record, datefmt=None):
        ct = datetime.fromtimestamp(record.created, self.timezone)
        return time.strftime(datefmt or "%Y-%m-%d %H:%M:%S", ct.timetuple())

# This is my formatter with special colors and Melbourne (AUS) timezone
#  ssardina - Sebastian Sardina - ssardina@gmail.com
formatter_ssardina = IndentColorFormatter(
    fmt=LOGGING_FMT,
    log_colors={
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "bold_red",
    },
    timezone=MELBOURNE_TZ,
    datefmt=LOGGING_DATE,
)

# logging.setLoggerClass(IndentLogger)

# handler = logging.StreamHandler()
# handler.setFormatter(formatter_ssardina)

# logger = logging.getLogger("nested_color_logger")
# logger.propagate = False  # Prevent logs from bubbling to root logger
# logger.handlers = []  # Clear any previous handlers
# logger.addHandler(handler)

# # logger.setLevel(logging.DEBUG)
# handler.setLevel(logging.INFO)  # 👈 controls what the handler will emit

# # handler.setLevel(logging.DEBUG)
# # logger.root.setLevel(logging.INFO)
