from __future__ import annotations

import os

from raya.entry_point import entry_point

from src.app import RayaApplication


def main():
    app_path = os.path.dirname(os.path.realpath(__file__))
    entry_point(app_path, RayaApplication)


if __name__ == '__main__':
    main()
