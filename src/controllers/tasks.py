from flask import Blueprint, request
import jsonpickle

taskController = Blueprint('task_controller', __name__, template_folder='templates')

@taskController.route('/api/v1/item', methods=['GET'])
def item():
    return jsonpickle.encode({'item': 'item1'}, unpicklable=False)