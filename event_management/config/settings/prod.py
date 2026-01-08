"""Production settings."""
from __future__ import annotations

import os

from .base import *  # noqa

DEBUG = False
ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "").split(",")

