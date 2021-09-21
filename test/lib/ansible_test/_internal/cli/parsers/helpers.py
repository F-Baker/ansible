"""Helper functions for composite parsers."""
from __future__ import annotations

import typing as t

from ...constants import (
    CONTROLLER_PYTHON_VERSIONS,
    SUPPORTED_PYTHON_VERSIONS,
)

from ...completion import (
    DOCKER_COMPLETION,
    REMOTE_COMPLETION,
    filter_completion,
)

from ...host_configs import (
    DockerConfig,
    HostConfig,
    PosixRemoteConfig,
)


def get_docker_pythons(name, controller, strict):  # type: (str, bool, bool) -> t.List[str]
    """Return a list of docker instance Python versions supported by the specified host config."""
    image_config = filter_completion(DOCKER_COMPLETION).get(name)
    available_pythons = CONTROLLER_PYTHON_VERSIONS if controller else SUPPORTED_PYTHON_VERSIONS

    if not image_config:
        return [] if strict else available_pythons

    supported_pythons = [python for python in image_config.supported_pythons if python in available_pythons]

    return supported_pythons


def get_remote_pythons(name, controller, strict):  # type: (str, bool, bool) -> t.List[str]
    """Return a list of remote instance Python versions supported by the specified host config."""
    platform_config = filter_completion(REMOTE_COMPLETION).get(name)
    available_pythons = CONTROLLER_PYTHON_VERSIONS if controller else SUPPORTED_PYTHON_VERSIONS

    if not platform_config:
        return [] if strict else available_pythons

    supported_pythons = [python for python in platform_config.supported_pythons if python in available_pythons]

    return supported_pythons


def get_controller_pythons(controller_config, strict):  # type: (HostConfig, bool) -> t.List[str]
    """Return a list of controller Python versions supported by the specified host config."""
    if isinstance(controller_config, DockerConfig):
        pythons = get_docker_pythons(controller_config.name, False, strict)
    elif isinstance(controller_config, PosixRemoteConfig):
        pythons = get_remote_pythons(controller_config.name, False, strict)
    else:
        pythons = SUPPORTED_PYTHON_VERSIONS

    return pythons
