"""Minimal HTTP server exposing the Dress Code Now pipeline."""

from __future__ import annotations

import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Callable, Dict

from app import api

ROUTES: Dict[tuple[str, str], Callable[[dict], dict]] = {
    ("POST", "/api/dress-code"): api.infer_dress_code,
    ("POST", "/api/recommendations"): api.recommend_outfit,
    ("POST", "/api/outfit-pipeline"): api.run_outfit_pipeline,
}


class DressCodeRequestHandler(BaseHTTPRequestHandler):
    server_version = "DressCodeNow/0.1"

    def _set_headers(self, status: HTTPStatus = HTTPStatus.OK) -> None:
        self.send_response(status.value)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

    def do_OPTIONS(self) -> None:  # noqa: N802 - required by BaseHTTPRequestHandler
        self.send_response(HTTPStatus.NO_CONTENT.value)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self) -> None:  # noqa: N802 - required by BaseHTTPRequestHandler
        route = ("POST", self.path)
        handler = ROUTES.get(route)
        if handler is None:
            self._set_headers(HTTPStatus.NOT_FOUND)
            self.wfile.write(b"{\"error\": \"Not found\"}")
            return

        content_length = int(self.headers.get("Content-Length", "0"))
        raw_body = self.rfile.read(content_length) if content_length else b"{}"

        try:
            payload = json.loads(raw_body.decode("utf-8")) if raw_body else {}
        except json.JSONDecodeError:
            self._set_headers(HTTPStatus.BAD_REQUEST)
            self.wfile.write(b"{\"error\": \"Invalid JSON payload\"}")
            return

        try:
            result = handler(payload)
        except (KeyError, ValueError) as exc:
            self._set_headers(HTTPStatus.BAD_REQUEST)
            message = json.dumps({"error": str(exc)})
            self.wfile.write(message.encode("utf-8"))
            return

        self._set_headers(HTTPStatus.OK)
        self.wfile.write(json.dumps(result).encode("utf-8"))


def run(host: str = "127.0.0.1", port: int = 8000) -> None:
    with HTTPServer((host, port), DressCodeRequestHandler) as httpd:
        print(f"Serving Dress Code Now on http://{host}:{port}")
        httpd.serve_forever()


if __name__ == "__main__":
    run()
