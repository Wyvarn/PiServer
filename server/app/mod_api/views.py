from . import api


@api.route("orange/<task>")
def orange(task):
    return task
