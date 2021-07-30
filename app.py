from flask import Flask
from website import create_app, log


if __name__ == "__main__":
    app: Flask = create_app()
    log.info("Starting the app")
    app.run(debug=True)
