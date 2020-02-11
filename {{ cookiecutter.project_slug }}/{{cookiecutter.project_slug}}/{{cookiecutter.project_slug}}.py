import sys

import click
import dotenv

from bda_project.tools import init_logger, logging

LOGGER = logging.getLogger(__name__)

@click.command(short_help="{{ cookiecutter.project_short_description }}")
def main():
    pass  # TODO

if __name__ == '__main__':
    init_logger(LOGGER, logging.INFO)

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    if not hasattr(sys, 'frozen') and hasattr(sys, '_MEIPASS'):
        dotenv.load_dotenv(dotenv.find_dotenv())

    sys.exit(main(standalone_mode=False))  # pylint: disable=no-value-for-parameter,unexpected-keyword-arg
