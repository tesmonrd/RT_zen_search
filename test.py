from app import app
from rt_zen_search.db_setup import init_db


init_db()


@app.route('/')
def test():
	return "We here!"

if __name__ == '__main__':
	app.run()
