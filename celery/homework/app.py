import os
from os.path import join, dirname, realpath
from celery import group
from flask import Flask, request, jsonify
from celery_conf import process_images, celery_app
from mail import send_email_for_subscribed
from models import User

app = Flask(__name__)

UPLOAD_FOLDER = join(dirname(realpath(__file__)))
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/blur', methods=["POST"])
def blur_image_request():
    """
    This is an endpoint get image files and email, then send blured images on email.
    """
    if request.method == 'POST':
        if 'image' not in request.files:
            return 'Image file was not uploaded', 400
        elif 'email' not in request.form:
            return 'Email field is empty'
        images = request.files.getlist('image')
        email = request.form['email']

        filenames = [image.filename for image in images]
        for image, filename in zip(images, filenames):
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        task_group = group(
            process_images.s(filename, email)
            for filename in filenames
        )

        result = task_group.apply_async()
        result.save()  # Запускаем группу задач и сохраняем её

        return jsonify({'group_id': result.id}), 202


@app.route('/status/<group_id>', methods=['GET'])
def get_status(group_id: str):
    result = celery_app.GroupResult.restore(group_id)
    if result:
        completed_count = result.completed_count()
        total_tasks = len(result)
        status = "обработка" if completed_count < total_tasks else "завершено"

        return jsonify({
            "status": status,
            "progress": f"{completed_count}/{total_tasks}",
        }), 200
    else:
        return jsonify({'error': 'Недопустимый group_id'}), 404


@app.route('/subscribe', methods=["POST"])
def subscribed():
    """
    This is an endpoint get email and subscribe it weekly mailing.
    """
    if request.method == 'POST':
        email = request.form.get("email")
        User.set_user_subscribed(email)
        return 'OK', 200


@app.route('/unsubscribe', methods=["POST"])
def unsubscribed():
    """
    This is an endpoint get email and unsubscribe it weekly mailing.
    """
    if request.method == 'POST':
        email = request.form.get("email")
        User.set_user_unsubscribed(email)
        return 'OK', 200


@app.route('/', methods=["GET"])
def ss():
    victims = User.get_subscribed_users()
    for user in victims:
        send_email_for_subscribed(user.email)

    return 'OK'



if __name__ == '__main__':
    app.run(debug=True)
