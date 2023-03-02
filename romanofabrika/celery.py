import os
from celery import Celery

app = Celery('tasks', backend='amqp', broker='amqp://')

@app.task(ignore_result=True)
def testTask():
    print("hello task")
    
@app.task
def gen_prime(x):
    multiples = []
    results = []
    for i in range(2, x+1):
        if i not in multiples:
            results.append(i)
            for j in range(i*i, x+1, i):
                multiples.append(j)
    return results