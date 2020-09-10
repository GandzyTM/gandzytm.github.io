import sentry_sdk
import logging

from bottle import Bottle, request, HTTPResponse
from sentry_sdk.integrations.bottle import BottleIntegration

sentry_sdk.init(
    dsn="https://c9688d3e2d304e1aa571bc07793fe23d@o439155.ingest.sentry.io/5405416",
    integrations=[BottleIntegration()]
)

app = Bottle()


# TODO
#   /success, который должен возвращать как минимум HTTP ответ со статусом 200 OK
#   /fail, который должен возвращать "ошибку сервера" (на стороне Bottle это может быть просто RuntimeError), то есть HTTP ответ со статусом 500

@app.route('/success')
def success():

    return "Success"


@app.route('/fail')
def fail():
    raise RuntimeError("HTTP error 500")


@app.route('/')
def index():
    return "OK"

def main():
    app.run(host='localhost', port=8080)


if __name__ == "__main__":
    main()
