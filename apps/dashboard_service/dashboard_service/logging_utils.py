# Copyright (C) 2024 Archimedes Exhibitions GmbH,
# Saarbrücker Str. 24, Berlin, Germany
#
# This file contains proprietary source code and confidential
# information. Its contents may not be disclosed or distributed to
# third parties unless prior specific permission by Archimedes
# Exhibitions GmbH, Berlin, Germany is obtained in writing. This
# applies to copies made in any form and using any medium. It applies
# to partial as well as complete copies.
import logging


def setup_logging(log_levels: list[str]) -> None:
    logging.basicConfig(
        level=logging.WARNING,
        format="[{asctime}] {levelname:.4} {{{name}:{lineno}}} {message}",
        style="{",
    )

    for log_level in log_levels:
        configure_log_level(log_level)


def configure_log_level(log_level: str) -> None:
    delimiter = ":"

    if delimiter not in log_level:
        raise RuntimeError(
            f"Log-level '{log_level}' is not in the required format 'component:level'"
        )

    component, level = log_level.strip().lower().split(delimiter)

    level = level.upper()
    numeric_level = getattr(logging, level, None)

    if not isinstance(numeric_level, int):
        raise RuntimeError(f"Log level {level} could not be found")
    if component == "root":
        logging.getLogger(name=None).setLevel(numeric_level)
    else:
        logging.getLogger(name=component).setLevel(numeric_level)
