"""Aplicação Flask mínima usada para exercitar o pipeline de segurança.

Mantida intencionalmente simples para que o workflow rode end-to-end sem
ruído. Veja docs/PIPELINE.md para o detalhamento de cada job.
"""
from __future__ import annotations

import os

from flask import Flask, jsonify

app = Flask(__name__)


@app.get("/health")
def health() -> tuple[dict, int]:
    return jsonify(status="ok"), 200


@app.get("/version")
def version() -> tuple[dict, int]:
    return jsonify(version=os.environ.get("APP_VERSION", "dev")), 200


def main() -> None:
    port = int(os.environ.get("PORT", "8000"))
    app.run(host="127.0.0.1", port=port)


if __name__ == "__main__":
    main()
