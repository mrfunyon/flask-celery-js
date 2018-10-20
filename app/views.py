from flask import Blueprint, render_template, abort, jsonify
from jinja2 import TemplateNotFound

views = Blueprint('views', __name__,
                        template_folder='templates')


@views.route('/', defaults={'page': 'index'})
@views.route('/<page>')
def show(page):
    try:
        return render_template('pages/%s.html' % page)
    except TemplateNotFound:
        abort(404)

@views.route('/send/work')
@views.route('/send/work/')
def send_work():
    from .tasks import test_task

    t = test_task.delay()
    j = jsonify({'task_id': t.id})
    return j


@views.route('/check/work/<tid>', defaults={'is_async': 't'})
@views.route('/check/work/<tid>/<is_async>')
def check_work(tid, is_async):
    from .tasks import celery
    result = celery.AsyncResult(tid)
    print(celery.conf.result_backend)
    if is_async == 't':
        if result.ready():
            # res = repr(result.result).decode("unicode-escape")
            return jsonify({'status':'ready', 'result': result.result})
    else:
        while not result.ready():
            import time
            time.sleep(.5)
        return jsonify({'status':'ready', 'result': result.result})
    return jsonify({'status': 'Not ready'})

