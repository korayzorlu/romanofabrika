# Create your tasks here


from celery import shared_task

from romanofabrika.celery import app

from .models import Product, Category
from django_celery_results.models import TaskResult

@shared_task
def add():
    print("hello taskk")
    return "hello task"