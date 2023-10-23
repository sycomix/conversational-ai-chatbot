"""
 Copyright (C) 2021 Intel Corporation
 SPDX-License-Identifier: BSD-3-Clause
"""

from envparse import Env
from zmq_integration_lib import get_inpad, get_outpad


def _validate_env_addr_variable(INPUT_ADDR, OUTPUT_ADDR, AUTHZ_SERVER_ADDR):
    for variable in [INPUT_ADDR, OUTPUT_ADDR, AUTHZ_SERVER_ADDR]:
        if (
            type(variable) != str
            or len(variable.split()) != 1
            or "tcp" not in variable.split(":")
            and "ipc" not in variable.split(":")
        ):
            raise ValueError(f"Please check {variable} address")


def _validate_env_topic_variable(INPUT_TOPIC, OUTPUT_TOPIC):
    for variable in [INPUT_TOPIC, OUTPUT_TOPIC]:
        if type(variable) != str or len(variable.split()) != 1:
            raise ValueError(f"Please check {variable} topic")


def _validate_env_log_level_variable(LOG_LEVEL):
    if (
        LOG_LEVEL.lower() not in ["info", "error", "debug"]
        or len(LOG_LEVEL.split()) != 1
    ):
        raise ValueError("Please provide correct Log level")


def get_inputport():
    return get_inpad(INPUT_ADDR, INPUT_TOPIC, AUTHZ_SERVER_ADDR)


def get_outputport():
    return get_outpad(OUTPUT_ADDR, OUTPUT_TOPIC)


def display_help():
    print("The application needs the following environment variables.")
    print("INPUT_ADDR, INPUT_TOPIC, OUTPUT_ADDR, OUTPUT_TOPIC")
    print("Please set the variables and try again.")


def _read_env_variables():
    # Can set schema
    env = Env(
        INPUT_ADDR=str,
        INPUT_TOPIC=str,
        OUTPUT_ADDR=str,
        OUTPUT_TOPIC=str,
        AUTHZ_SERVER_ADDR=str,
        LOG_LEVEL=dict(cast=str, default="ERROR"),
    )

    # Read env variables
    INPUT_ADDR = env("INPUT_ADDR")
    INPUT_TOPIC = env("INPUT_TOPIC")
    OUTPUT_ADDR = env("OUTPUT_ADDR")
    OUTPUT_TOPIC = env("OUTPUT_TOPIC")
    AUTHZ_SERVER_ADDR = env("AUTHZ_SERVER_ADDR")
    LOG_LEVEL = env("LOG_LEVEL")

    # Validate env addr variable
    _validate_env_addr_variable(INPUT_ADDR, OUTPUT_ADDR, AUTHZ_SERVER_ADDR)

    # Validate env topic variable
    _validate_env_topic_variable(INPUT_TOPIC, OUTPUT_TOPIC)

    # Validate env log level variable
    _validate_env_log_level_variable(LOG_LEVEL)
    return (
        INPUT_ADDR,
        INPUT_TOPIC,
        OUTPUT_ADDR,
        OUTPUT_TOPIC,
        AUTHZ_SERVER_ADDR,
        LOG_LEVEL,
    )


def get_logger():
    import logging

    global LOG_LEVEL  # string
    level = logging.ERROR
    if LOG_LEVEL.upper() == "WARNING":
        level = logging.WARNING
    if LOG_LEVEL.upper() == "DEBUG":
        level = logging.DEBUG
    if LOG_LEVEL.upper() == "INFO":
        level = logging.INFO

    logging.basicConfig(
        # format="%(asctime)s - %(levelname)s - %(message)s", level=level)
        format="%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)s - %(funcName)-20s ] - %(message)s",
        level=level,
    )
    logging.root.setLevel(level)
    logger = logging.getLogger()
    logger.setLevel(level)
    return logger


(
    INPUT_ADDR,
    INPUT_TOPIC,
    OUTPUT_ADDR,
    OUTPUT_TOPIC,
    AUTHZ_SERVER_ADDR,
    LOG_LEVEL,
) = _read_env_variables()
