
'''
@author: tres
'''
from sets import Set
import pickle
import sys
from datetime import datetime
from functools import partial
from flask import Blueprint, render_template, request, jsonify, \
    url_for, session, redirect, abort
from pymongo import Connection
from pymongo.objectid import ObjectId
from demo.models.documents import Todo
from demo import db, redis_cli
import json

api = Blueprint('api', __name__, 
        template_folder='demo/templates', static_folder='static')


def remove_OIDs(obj, recursive=False):
    """
    Removes the ObjectID types from an object 
    before returning
    """
    if isinstance(obj, list):
        return [remove_OIDs(ob) for ob in obj]
    elif isinstance(obj, db.Document):
        return obj.clean4_dump()


def redis_save(savee, key_field='', value_fields=(), serializer=str, deserializer=dict, store_func=set):
    loaded_str = redis_cli.get('school_hash')
    hashed = pickle.loads(loaded_str) if loaded_str is not None else {}
    dlist_keys = lambda obj, key: {key: obj}
    if hasattr(savee, '_field_values'):
        savee = savee._field_values
    base = [savee]
    for keyf in reversed(value_fields):
        base = dlist_keys(base, keyf)
    search = hashed
    for keyf in value_fields:
        if keyf not in search:
            search[keyf] = base[keyf]
        elif isinstance(base[keyf], list):
            search[keyf] = base[keyf] + search[keyf] if base[keyf] != search[keyf] else search[keyf]
        search = search[keyf]
        base = base[keyf]
    savee['_id'] =  str(savee['_id'])
    redis_cli.set('school_hash', pickle.dumps(hashed) )    
    return base
   

@api.route('/todos', methods=['GET'])
def get_todos():
    return json.dumps( Todo.query.all(), default=remove_OIDs)

@api.route('/todos/<todo_id>', methods=['GET'])
def get_todo(todo_id):
    return json.dumps( Todo.query.filter(Todo.mongo_id == ObjectId(todo_id)).one(), default=remove_OIDs)


@api.route('/todos', methods=['POST'])
def create_todo():
    todo = Todo(mongo_id=ObjectId(), **request.data)
    todo.save()
    return json.dumps( todo, default=remove_OIDs)

@api.route('/todos/<todo_id>', methods=['PUT'])
def update_todo(todo_id):
    del request.data['id']
    todo = Todo(mongo_id=ObejctId(todo_id), **request.data)
    todo.save()
    return json.dumps( todo, default=remove_OIDs)

