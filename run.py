from common.utils import get_var
from flask_init import create_app

app = create_app()

if __name__ == '__main__':
    port = int(get_var('FLASK_PORT', 80))
    host = get_var('FLASK_HOST', '0.0.0.0')
    app.run(host=host, port=port)
