from flask import Flask, jsonify
from flask_restful import Api
from flask_cors import CORS
from threading import Thread

import os

DIRECTORY_RESOURCES = "app/modulo_cognitivo/api_v1_0/resources/*.py"


def create_app(settings_module):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(settings_module)
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
    # Inicializa las extensiones
    #db.init_app(app)
    #ma.init_app(app)
    #migrate.init_app(app, db)
    # Captura todos los errores 404
    Api(app, catch_all_404s=True)
    # Deshabilita el modo estricto de acabado de una URL con /
    app.url_map.strict_slashes = False
    
    # Registra los blueprints
    import glob 
    import importlib
    modules_name = glob.glob(DIRECTORY_RESOURCES)
    for i in modules_name:
        module = i.split(".")[0]
        module = module.replace("/",".")
        print(module)
        load_module = importlib.import_module(module)
        app.register_blueprint(load_module.getBlueprint())
        
    # Registra manejadores de errores personalizados
    register_error_handlers(app)
    #app.wsgi_app = Middleware(app.wsgi_app)
    return app

def register_error_handlers(app):
    @app.errorhandler(Exception)
    def handle_exception_error(e):
        return jsonify({'msg': 'Internal server error'}), 500
    @app.errorhandler(405)
    def handle_405_error(e):
        return jsonify({'msg': 'Method not allowed'}), 405
    @app.errorhandler(406)
    def handle_406_error(e):
        return jsonify({'msg': 'Bad syntaxis in JSON'}), 406
    @app.errorhandler(403)
    def handle_403_error(e):
        return jsonify({'msg': 'Forbidden error'}), 403
    @app.errorhandler(404)
    def handle_404_error(e):
        return jsonify({'msg': 'Not Found error'}), 404


if __name__ == "__main__":
    settings_module = os.getenv('APP_SETTINGS_MODULE')
    app = create_app(settings_module)
    p = Thread(target=app.run, kwargs={'host':"localhost"})
    p.start()