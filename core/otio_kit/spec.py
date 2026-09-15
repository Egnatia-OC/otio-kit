"""Spec v0 loading and validation. Loud failures only."""

import json
import pathlib

import jsonschema
import yaml

SCHEMA_PATH = pathlib.Path(__file__).parent / "schema" / "spec-v0.schema.json"


class SpecError(ValueError):
    """Spec is malformed or semantically invalid. Message is user-facing."""


class Spec:
    """A validated spec document plus the directory it was loaded from."""

    def __init__(self, data: dict, path: pathlib.Path):
        self.data = data
        self.path = path
        self.base_dir = path.parent
        self.fps = data["fps"]
        self.name = data["name"]
        self.media = data["media"]
        self.timeline = data["timeline"]
        self.markers = data.get("markers", [])


def load_spec(path: str | pathlib.Path) -> Spec:
    """Load a spec YAML file, validate it against the v0 schema, and run
    semantic checks. Raises SpecError with an actionable message."""
    path = pathlib.Path(path)
    if not path.is_file():
        raise SpecError(f"spec file not found: {path}")

    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise SpecError(f"invalid YAML in {path}:\n{exc}") from exc

    if not isinstance(data, dict):
        raise SpecError(f"{path}: top level must be a mapping")

    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    try:
        jsonschema.validate(instance=data, schema=schema)
    except jsonschema.ValidationError as exc:
        where = "/".join(str(p) for p in exc.absolute_path) or "(top level)"
        raise SpecError(f"{path}: schema violation at {where}: {exc.message}") from exc

    _semantic_checks(data)
    return Spec(data, path)


def _semantic_checks(data: dict) -> None:
    media_keys = set(data["media"])
    problems = []
    for section in ("video", "audio"):
        for track in data["timeline"].get(section, []):
            clips = track["clips"]
            for i, clip in enumerate(clips):
                if clip["media"] not in media_keys:
                    problems.append(
                        f"track {track['track']!r} clip {i}: media key "
                        f"{clip['media']!r} not defined in media map"
                    )
                if section == "video" and i == 0 and "transition_in" in clip:
                    problems.append(
                        f"track {track['track']!r}: transition_in on the first "
                        "clip has nothing to transition from"
                    )
    if problems:
        raise SpecError(f"{len(problems)} problem(s):\n  - " + "\n  - ".join(problems))
