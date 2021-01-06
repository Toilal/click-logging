Click-logging
=============

**Simple and beautiful logging for click applications**

[![PyPI](https://img.shields.io/pypi/v/click-logging)](https://pypi.org/project/click-logging/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/click-logging)](https://pypi.org/project/click-logging/)
[![PyPI - License](https://img.shields.io/pypi/l/click-logging)](https://github.com/Toilal/click-logging/blob/develop/LICENSE)
[![Build Status](https://github.com/Toilal/click-logging/workflows/build/badge.svg)](https://github.com/Toilal/click-logging/actions?query=workflow%3Abuild)
[![Code coverage](https://img.shields.io/coveralls/github/Toilal/click-logging)](https://coveralls.io/github/Toilal/click-logging)
[![semantic-release](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--release-e10079.svg)](https://github.com/relekang/python-semantic-release)


Integrates logging with click.

Project sources and documentation are available on [Github](https://github.com/Toilal/click-logging)

Documentation
=============

Getting started
---------------

Assuming you have this Click application:

    @click.command()
    def cli():
        click.echo("Dividing by zero.")

        try:
            1 / 0
        except:
            click.echo("ERROR: Failed to divide by zero.")

Ignore the application's core functionality for a moment. The much more pressing question here is: How do we add an option to not print anything on success? We could try this:

    @click.command()
    @click.option('--quiet', default=False, is_flag=True)
    def cli(quiet):
        if not quiet:
            click.echo("Dividing by zero.")

        try:
            1 / 0
        except:
            click.echo("ERROR: Failed to divide by zero.")

Wrapping if-statements around each `echo`-call is cumbersome though. And with that, we discover logging:

    import logging
    logger = logging.getLogger(__name__)
    # More setup for logging handlers here

    @click.command()
    @click.option('--quiet', default=False, is_flag=True)
    def cli(quiet):
        if quiet:
            logger.setLevel(logging.ERROR)
        else:
            logger.setLevel(logging.INFO)

        ...

Logging is a better solution, but partly because Python's logging module aims to be so generic, it doesn't come with sensible defaults for CLI applications. At some point you might also want to expose more logging levels through more options, at which point the boilerplate code grows even more.

This is where click-logging comes in:

```python
import logging
import click
import click_logging

logger = logging.getLogger(__name__)
click_logging.basic_config(logger)
@click.command()
@click_logging.simple_verbosity_option(logger)
def cli():
    logger.info("Dividing by zero.")

    try:
        1 / 0
    except:
        logger.error("Failed to divide by zero.")
```

The output will look like this:

    Dividing by zero.
    error: Failed to divide by zero.

The `error:`-prefix will be red, unless the output is piped to another command.

The :pysimple\_verbosity\_option decorator adds a `--verbosity` option that takes a (case-insensitive) value of `DEBUG`, `INFO`, `WARNING`, `ERROR`, or `CRITICAL`, and calls `setLevel` on the given logger accordingly.

> **note**
>
> Make sure to define the simple\_verbosity\_option as early as possible. Otherwise logging setup will not be early enough for some of your other eager options.

Customize output
---

You can customize [click styles](https://click.palletsprojects.com/en/7.x/api/#utilities) for each log level with 
`style_kwargs` keyword argument of `basic_config` function.

```python
import logging
import click_logging

logger = logging.getLogger(__name__)
style_kwargs = {
    'error': dict(fg='red', blink=True),
    'exception': dict(fg='red', blink=True),
    'critical': dict(fg='red', blink=True)
}
click_logging.basic_config(logger, style_kwargs=style_kwargs)
```

You can customize [click echo](https://click.palletsprojects.com/en/7.x/api/#utilities) to stderr using `echo_kwargs` keyword argument of `basic_config` function.

```python
import logging
import click_logging

logger = logging.getLogger(__name__)
echo_kwargs = {
    'error': dict(err=True),
    'exception': dict(err=True),
    'critical': dict(err=True),
}
click_logging.basic_config(logger, echo_kwargs=True)
```

API
---

### Classes

Indices and tables
------------------

-   genindex
-   modindex
-   search

Fork
====

This is a fork of [click-contrib/click-log](https://github.com/click-contrib/click-log)

Motivations of the fork:
- semantic-release and github actions to merge and release often.
- more configuration options.

License
=======

Licensed under the MIT, see `LICENSE`.
