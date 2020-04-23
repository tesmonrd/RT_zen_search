from flask import Flask
from rt_zen_search.models import db
from rt_zen_search.route_bp import bp
from rt_zen_search.db_setup import init_db


app = Flask(
	__name__,
	template_folder='rt_zen_search/templates',
	static_folder='rt_zen_search/static')
app.config.from_object('config.AppConfig')
init_db()
db.init_app(app)
app.register_blueprint(bp)

if __name__ == '__main__':
	app.run()
