from django.shortcuts import get_object_or_404

from .models import Sprint

def can_add_task_to_sprint(task, sprint_id):
    """ 
    Checks if a task can be added to a sprint based on the
    sprint's date range.
    """
    sprint = get_object_or_404(Sprint, id=sprint_id)
    return sprint.start_date <= task.created_ad.date() <= sprint.end_date