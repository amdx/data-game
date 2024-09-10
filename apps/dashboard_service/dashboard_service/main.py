# Copyright (C) 2024 Archimedes Exhibitions GmbH,
# Saarbrücker Str. 24, Berlin, Germany
#
# This file contains proprietary source code and confidential
# information. Its contents may not be disclosed or distributed to
# third parties unless prior specific permission by Archimedes
# Exhibitions GmbH, Berlin, Germany is obtained in writing. This
# applies to copies made in any form and using any medium. It applies
# to partial as well as complete copies.

import contextlib
import logging

from fastapi import FastAPI

from dashboard_service import api
from dashboard_service import configs
from dashboard_service import logging_utils

logger = logging.getLogger(__name__)


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    # Preload configuration
    config = configs.get_config()
    logging_utils.setup_logging(config.log_levels)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(api.router, prefix="/api/v1")
