import logging
import logging.config
import os
import sys

import concurrent_log_handler  # noqa: F401 # type: ignore
import torch

# log.conf adds rotating files under .log/ on top of console output. It's
# optional: the Docker image doesn't ship it, so there logs only go to stdout
# (and to OTel when OTEL_EXPORTER_OTLP_ENDPOINT is set, see teg.telemetry).
LOG_CONF = os.getenv("TEG_LOG_CONF", "./log.conf")

if os.path.exists(LOG_CONF):
    # ConcurrentRotatingFileHandler doesn't create the directory, and without
    # it file logging fails silently (only a "--- Logging error ---" traceback
    # on stderr).
    os.makedirs(".log", exist_ok=True)
    logging.config.fileConfig(LOG_CONF, disable_existing_loggers=False)
else:
    logging.basicConfig(
        level=logging.INFO,
        stream=sys.stdout,
        format="[%(levelname)s] %(asctime)s [%(process)d] %(name)s.%(funcName)s: %(lineno)d %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S(%Z)",
    )


logger = logging.getLogger("root")
device = torch.device(
    "cuda"
    if torch.cuda.is_available()
    else "mps"
    if torch.backends.mps.is_available()
    else "cpu"
)
logger.info(f"Using device: {device}")
