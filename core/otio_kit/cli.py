"""otio-kit command line interface."""

import argparse
import sys

from . import __version__
from .emit_otio import EmitError, emit, write_otio
from .media import MediaMissingError, resolve_media
from .spec import SpecError, load_spec


def _compile(args) -> int:
    try:
        spec = load_spec(args.spec)
        media = resolve_media(spec)
        timeline = emit(spec, media)
        out = write_otio(timeline, args.output)
    except (SpecError, MediaMissingError, EmitError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    n_clips = sum(len(t["clips"]) for t in spec.timeline.get("video", []))
    n_clips += sum(len(t["clips"]) for t in spec.timeline.get("audio", []))
    print(f"compiled {spec.name!r}: {n_clips} clips, "
          f"{len(spec.timeline.get('video', [])) + len(spec.timeline.get('audio', []))} tracks "
          f"-> {out}")
    return 0


def _validate(args) -> int:
    try:
        spec = load_spec(args.spec)
        resolve_media(spec)
    except (SpecError, MediaMissingError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(f"ok: {spec.name!r} ({args.spec})")
    return 0


def _support(args) -> int:
    print(
        "otio-kit is a public record of what survives on DaVinci Resolve Free.\n"
        "It is free and stays free.\n"
        "\n"
        "Project, docs, and the per-release fidelity log:\n"
        "    https://github.com/Egnatia-OC/otio-kit\n"
        "\n"
        "Support the project (patronage for the re-test cadence — no perks,\n"
        "no unlock) and get notified when the flagship ships:\n"
        "    https://github.com/Egnatia-OC/otio-kit#support-the-project"
    )
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="otio-kit",
        description="Compile timeline briefs into OTIO that imports cleanly "
                    "into DaVinci Resolve Free. Not affiliated with Blackmagic Design.",
    )
    parser.add_argument("--version", action="version", version=__version__)
    sub = parser.add_subparsers(dest="command", required=True)

    p_compile = sub.add_parser("compile", help="spec YAML -> .otio")
    p_compile.add_argument("spec", help="spec YAML file")
    p_compile.add_argument("-o", "--output", help="output .otio path "
                           "(default: <spec dir>/<name>.otio)")
    p_compile.set_defaults(func=_compile)

    p_validate = sub.add_parser("validate", help="validate spec + media, no output")
    p_validate.add_argument("spec", help="spec YAML file")
    p_validate.set_defaults(func=_validate)
    p_support = sub.add_parser("support",
                               help="project, support, and updates")
    p_support.set_defaults(func=_support)


    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
