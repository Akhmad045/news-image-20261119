#!/usr/bin/env python3
"""Entry point for the news-image-20261119 make.fun bounty (program/v1).

Copies the pre-rendered front-page image (entry.png, sitting beside this
file in the repository) to the output directory as entry.png.

Standard library only, no network, fully deterministic: the same bytes are
written on every run.
"""
import os
import shutil

# The image lives next to this script in the repository.
HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")


def main():
    # MAKEFUN_OUTPUT_DIR is set by the grader; default /output matches the
    # competition spec when the variable is absent.
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    # copyfile (not copy) so no metadata is carried over: output bytes are
    # exactly the repository image's bytes, every run.
    shutil.copyfile(SOURCE, dest)


if __name__ == "__main__":
    main()
