@app.task(bind=True, name='refresh')
def test(self):
    return "Hello Celery"