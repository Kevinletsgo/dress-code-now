"""Compatibility shim that exposes the HTTP server entry point."""

from __future__ import annotations

from app.server import run


def start() -> None:
    """Start the Dress Code Now HTTP server using default settings."""

    run()


if __name__ == "__main__":
    start()
