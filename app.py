from flask import Flask
from flask_url_mapping import FlaskUrls

from database import init_db
from urls import urls

app = Flask(__name__)

flask_urls = FlaskUrls(app)
flask_urls.register_urls(urls)

# Create DB
init_db()

if __name__ == '__main__':
    app.run()
    # app.run(host='0.0.0.0')