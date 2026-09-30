import json
import os
import sys

import psycopg

APP_VERSION = "1.1.0"
MESSAGE = "Hello from week 4"


def record_visit():
    with psycopg.connect(
        host=os.environ["DB_HOST"],
        port=int(os.environ["DB_PORT"]),
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        connect_timeout=3,
    ) as connection:
        row = connection.execute(
            "UPDATE counter SET visits = visits + 1 "
            "WHERE id = 1 RETURNING visits"
        ).fetchone()
        if row is None:
            raise psycopg.DatabaseError("Counter row is missing")
        return row[0]


def app(environ, start_response):
    if environ.get("PATH_INFO", "/") != "/":
        status = "404 Not Found"
        payload = {"error": "not found"}
    elif environ.get("REQUEST_METHOD", "GET") != "GET":
        status = "405 Method Not Allowed"
        payload = {"error": "use GET for this demonstration"}
    else:
        try:
            visits = record_visit()
            status = "200 OK"
            payload = {
                "application": "ica0022",
                "version": APP_VERSION,
                "message": MESSAGE,
                "visits": visits,
            }
        except psycopg.Error as error:
            print(f"Database error: {error}", file=sys.stderr, flush=True)
            status = "503 Service Unavailable"
            payload = {"error": "database unavailable; inspect the app logs"}

    body = (json.dumps(payload) + "\n").encode("utf-8")
    headers = [
        ("Content-Type", "application/json; charset=utf-8"),
        ("Content-Length", str(len(body))),
        ("Cache-Control", "no-store"),
    ]
    if status.startswith("405"):
        headers.append(("Allow", "GET"))
    start_response(status, headers)
    return [body]