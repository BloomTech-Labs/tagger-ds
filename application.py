from tagger import create_app
import logging

# Thread level logging for production debugging
logging.basicConfig(
    level=logging.DEBUG, format='%(relativeCreated)6d %(processName)s %(threadName)s %(message)s'
)

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0")
