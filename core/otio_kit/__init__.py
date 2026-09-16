"""otio-kit: compile timeline briefs into files that import cleanly into
DaVinci Resolve Free - no scripting bridge, no Studio required.

Not affiliated with or endorsed by Blackmagic Design.
"""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("otio-kit")
except PackageNotFoundError:  # imported from a source checkout, not installed
    __version__ = "unknown"
