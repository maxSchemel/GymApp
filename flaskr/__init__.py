import os
from flask import Flask

def create_app(test_config=None):
    """
    Create and configure the Flask application.

    Args:
        test_config (dict, optional): The configuration for testing the application.
                                      Defaults to None.

    Returns:
        Flask: The configured Flask application.

    Raises:
        OSError: If the instance folder creation fails.

    Example:
        # Create the Flask application
        app = create_app()

    """

    # Create the Flask application
    app = Flask(__name__, instance_relative_config=True)

    # Set the default configuration values
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)

    try:
        # Ensure the instance folder exists
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Initialize the database
    from GymApp.flaskr.src.database import db
    db.init_app(app)

    # Register the authentication blueprint
    from GymApp.flaskr.src.views import auth
    app.register_blueprint(auth.bp)

    # Register the main blueprint
    from GymApp.flaskr.src.views import main
    app.register_blueprint(main.bp)
    app.add_url_rule('/', endpoint='index')

    # Register the workout_view blueprint
    from GymApp.flaskr.src.views import workout_view
    app.register_blueprint(workout_view.bp)

    return app
