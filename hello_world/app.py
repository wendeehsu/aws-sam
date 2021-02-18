import json
import boto3
from flask import request, jsonify
from flask_lambda import FlaskLambda

app = FlaskLambda(__name__)
ddb = boto3.resource("dynamodb")
table = ddb.Table("students")

@app.route('/hello')
def index():
    data = {'message': 'Hello from aws'}
    return (
        jsonify(data),
        200,
        {'Content-Type': 'application/json'}
    )

@app.route('/students', methods=['GET', 'POST'])
def put_or_list_students():
    if request.method == "GET":
        students = table.scan()["Items"]
        return (
            jsonify(students),
            200,
            {'Content-Type': 'application/json'}
        )

    else:  #request.method == "POST"
        table.put_item(Item=request.form.to_dict())
        return (
            json.dumps({"message":"item inserted!"}),
            200,
            {'Content-Type': 'application/json'}
        )