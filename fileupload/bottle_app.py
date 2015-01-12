import json

from bottle import run, Bottle, request, response
from gridfs import GridFS
from pymongo import MongoClient


MONGO_CLIENT = MongoClient('mongodb://localhost:27017/')
ΩFILE_API = Bottle()
DB = MONGO_CLIENT['TestDB']
GRID_FS = GridFS(DB)


@FILE_API.put('/upload/<file_name>')
def upload(file_name):
    response.content_type = 'application/json'
    with GRID_FS.new_file(filename=file_name) as fp:
        fp.write(request.body)
        file_id = fp._id
    if GRID_FS.find_one(file_id) is not None:
        response.status = 200
        return json.dumps({'status': 'File saved successfully'})
    else:
        response.status = 500
        return json.dumps({'status': 'Error occurred while saving file.'})


@FILE_API.get('/download/<file_name>')
def index(file_name):
    grid_fs_file = GRID_FS.find_one({'filename': file_name})
    response.headers['Content-Type'] = 'application/octet-stream'
    response.headers["Content-Disposition"] = "attachment; filename={}".format(file_name)
    return grid_fs_file


run(app=FILE_API, host='localhost', port=8080)