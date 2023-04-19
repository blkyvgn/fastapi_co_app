from celery import Celery
from app.config import cfg


celery = Celery('tasks', backend=cfg.result_backend, broker=cfg.broker, include=['app.services.celery.tasks'])

celery.conf.update(
	task_serializer = cfg.task_serializer,
	accept_content = cfg.accept_content,
	task_queues = cfg.task_queues,
	task_default_queue = cfg.task_default_queue,
	task_default_exchange = cfg.task_default_exchange,
	task_default_routing_key = cfg.task_default_routing_key,
	task_routes = cfg.task_routes,
)


if __name__ == '__main__':
	celery.start()