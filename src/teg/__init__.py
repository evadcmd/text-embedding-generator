import logging.config

import concurrent_log_handler  # noqa: F401
import torch

logging.config.fileConfig("./log.conf", disable_existing_loggers=False)


logger = logging.getLogger("root")
device = torch.device(
    "cuda"
    if torch.cuda.is_available()
    else "mps"
    if torch.backends.mps.is_available()
    else "cpu"
)
logger.info(f"Using device: {device}")
