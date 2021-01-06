# -*- coding: utf-8 -*-

import logging
import sys

import click

_ctx = click.get_current_context

LOGGER_KEY = __name__ + '.logger'
DEFAULT_LEVEL = logging.INFO

PY2 = sys.version_info[0] == 2

if PY2:
    text_type = unicode  # noqa
else:
    text_type = str


def _meta():
    return _ctx().meta.setdefault(LOGGER_KEY, {})


class ColorFormatter(logging.Formatter):
    def __init__(self, style_kwargs):
        self.style_kwargs = style_kwargs

    def format(self, record):
        if not record.exc_info:
            level = record.levelname.lower()
            msg = record.getMessage()
            if self.style_kwargs.get(level):
                prefix = click.style('{}: '.format(level),
                                     **self.style_kwargs[level])
                msg = '\n'.join(prefix + x for x in msg.splitlines())
            return msg
        return logging.Formatter.format(self, record)


class ClickHandler(logging.Handler):
    def __init__(self, echo_kwargs):
        super().__init__()
        self.echo_kwargs = echo_kwargs

    def emit(self, record):
        try:
            msg = self.format(record)
            level = record.levelname.lower()
            if self.echo_kwargs.get(level):
                click.echo(msg, **self.echo_kwargs[level])
            else:
                click.echo(msg)
        except Exception:
            self.handleError(record)


def _normalize_logger(logger):
    if not isinstance(logger, logging.Logger):
        logger = logging.getLogger(logger)
    return logger


def _normalize_style_kwargs(styles):
    normalized_styles = {
        'error': dict(fg='red'),
        'exception': dict(fg='red'),
        'critical': dict(fg='red'),
        'debug': dict(fg='blue'),
        'warning': dict(fg='yellow')
    }
    if styles:
        normalized_styles.update(styles)
    return normalized_styles


def _normalize_echo_kwargs(echo_kwargs):
    normamized_echo_kwargs = dict()
    if echo_kwargs:
        normamized_echo_kwargs.update(echo_kwargs)
    return normamized_echo_kwargs


def basic_config(logger=None, style_kwargs=None, echo_kwargs=None):
    '''Set up the default handler (:py:class:`ClickHandler`) and formatter
    (:py:class:`ColorFormatter`) on the given logger.'''
    logger = _normalize_logger(logger)
    style_kwargs = _normalize_style_kwargs(style_kwargs)
    echo_kwargs = _normalize_echo_kwargs(echo_kwargs)

    handler = ClickHandler(echo_kwargs)
    handler.formatter = ColorFormatter(style_kwargs)
    logger.handlers = [handler]
    logger.propagate = False

    return logger
