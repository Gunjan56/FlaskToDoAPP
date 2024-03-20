from utils import create_app, register_routes

if __name__ == '__main__':
    app = create_app()
    register_routes(app)
    app.run(debug=True)
