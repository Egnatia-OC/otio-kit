"""Media manifest resolution. Missing media is a loud failure, never silent."""



class MediaMissingError(FileNotFoundError):
    """One or more media files referenced by the spec do not exist."""


def resolve_media(spec) -> dict[str, str]:
    """Resolve every media entry to an absolute path and verify it exists.

    Returns {logical name: absolute path}. Collects ALL missing entries into
    one error so the user fixes everything in a single pass.
    """
    resolved: dict[str, str] = {}
    missing: list[str] = []
    for name, rel in spec.media.items():
        p = (spec.base_dir / rel).resolve()
        if p.is_file():
            resolved[name] = str(p)
        else:
            missing.append(f"{name}: {p} (from {rel!r})")
    if missing:
        raise MediaMissingError(
            f"{len(missing)} media file(s) missing:\n  - " + "\n  - ".join(missing)
        )
    return resolved
