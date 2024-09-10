# Copyright (C) 2024 Archimedes Exhibitions GmbH,
# Saarbrücker Str. 24, Berlin, Germany
#
# This file contains proprietary source code and confidential
# information. Its contents may not be disclosed or distributed to
# third parties unless prior specific permission by Archimedes
# Exhibitions GmbH, Berlin, Germany is obtained in writing. This
# applies to copies made in any form and using any medium. It applies
# to partial as well as complete copies.
import click

from dashboard_service import configs


@click.command()
@click.option(
    "--dump-default-config",
    is_flag=True,
    required=True,
    help="Dump default configuration",
)
def cli(dump_default_config: bool):
    if dump_default_config:
        config = configs.build_default_config()
        configs.dump_config(config)


if __name__ == "__main__":
    cli()
