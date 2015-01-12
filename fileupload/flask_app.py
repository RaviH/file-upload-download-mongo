import json
from gridfs import GridFS
from pymongo import MongoClient
from flask import Flask, make_response
from flask import request

__author__ = 'ravihasija'

app = Flask(__name__)
mongo_client = MongoClient('mongodb://localhost:27017/')
db = mongo_client['TestDB']
grid_fs = GridFS(db)


@app.route('/upload/<file_name>', methods=['PUT'])
def upload(file_name):
    with grid_fs.new_file(filename=file_name) as fp:
        fp.write(request.data)
        file_id = fp._id

    if grid_fs.find_one(file_id) is not None:
        return json.dumps({'status': 'File saved successfully'}), 200
    else:
        return json.dumps({'status': 'Error occurred while saving file.'}), 500


@app.route('/download/<file_name>')
def index(file_name):
    grid_fs_file = grid_fs.find_one({'filename': file_name})
    response = make_response(grid_fs_file.read())
    response.headers['Content-Type'] = 'application/octet-stream'
    response.headers["Content-Disposition"] = "attachment; filename={}".format(file_name)
    return response


app.run(host="localhost", port=8081)