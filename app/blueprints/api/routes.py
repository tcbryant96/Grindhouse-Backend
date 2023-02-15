from . import api
from flask import jsonify, request, Response
from .auth import basic_auth, token_auth
from flask_cors import cross_origin
from app.models import User, Merch, Orders, Shows
from werkzeug.utils import secure_filename

@api.route('/token',  methods=['POST'])
@basic_auth.login_required
def get_token():
    user =basic_auth.current_user()
    token = user.get_token()
    return jsonify({'token': token})

@api.route('/admin', methods=['POST'])
def create_user():
    if not request.is_json:
        return jsonify({'error': 'Your request content-type must be application/json'}), 400
    data = request.json
    for user in ['username', 'email','password']:
        if user not in data:
            return jsonify({'error': f'{user} must be in request body'}), 400
    username = data.get('username')
    email = data.get('email')
    password = data.get("password")
    new_user= User(username=username, email=email, password=password)
    return jsonify(new_user.to_dict()), 201

@api.route('/shows', methods=['GET'])
def current_shows():
    pass

@api.route('/upload', methods=['POST'])
def upload():
    pic = request.files['pic']

    if not pic:
        return 'No pic uploaded', 400
    
    filename = secure_filename(pic.filename)
    mimetype = pic.mimetype
    merch = Merch(img=pic.read(), price= "9.99", mimetype=mimetype, name=filename)
    return "image uploaded successfully", 201

@api.route('/<int:id>')
def get_img(id):
    img = Merch.query.filter_by(id=id).first()
    if not img:
        return "no image with that id", 404

    return Response(img.img, img.mimetype)

