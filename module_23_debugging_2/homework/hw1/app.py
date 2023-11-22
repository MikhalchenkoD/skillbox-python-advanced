from flask import Flask
import sentry_sdk

sentry_sdk.init(
    dsn="https://5401d45d841cd08d176a4ac6a411fd91@o4506120091402240.ingest.sentry.io/4506120093106176",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)

app = Flask(__name__)

@app.route("/")
def hello_world():
  1/0  # raises an error
  return "<p>Hello, World!</p>"


if __name__ == '__main__':
    app.run()