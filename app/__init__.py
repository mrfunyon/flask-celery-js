from flask import Flask
from .views import views
from celery import Celery


CELERY_TASK_LIST = [
    'app.tasks',
]

def create_celery_app(app=None):
    """
    Create a new Celery object and tie together the Celery config to the app's
    config. Wrap all tasks in the context of the application.
    :param app: Flask app
    :return: Celery app
    """
    app = app or create_app()

    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'],
                    include=CELERY_TASK_LIST)

    celery.conf.update(app.config)
    celery.conf.result_backend=app.config['CELERY_BROKER_URL']

    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


def create_app():
    # Bail if we don't have a market name
    app = Flask(__name__, static_folder='../static')
    app.register_blueprint(views)
    app.config.update({
        'CELERY_BROKER_URL': "redis://redis/0",
    })
    from werkzeug.debug import DebuggedApplication
    app.wsgi_app = DebuggedApplication(app.wsgi_app, True)

    return app

app = create_app()