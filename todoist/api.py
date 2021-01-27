from typing import Any, Dict, List

import requests

from todoist.endpoints import TASKS_ENDPOINT, get_rest_url
from todoist.http_requests import delete, get, post
from todoist.models import Task
from todoist.utils import async_wrap


class TodoistAPI:
    def __init__(self, token: str, session=None):
        self._token: str = token
        self._session = session or requests.Session()

    def get_task(self, task_id: int) -> Task:
        endpoint = get_rest_url(f"{TASKS_ENDPOINT}/{task_id}")
        task = get(self._session, self._token, endpoint)
        return Task.from_dict(task)

    get_task_async = async_wrap(get_task)

    def get_tasks(self, **kwargs) -> List[Task]:
        ids = kwargs.pop("ids", None)

        if ids:
            kwargs.update({"ids": ",".join(str(i) for i in ids)})

        endpoint = get_rest_url(TASKS_ENDPOINT)
        tasks = get(self._session, self._token, endpoint, kwargs)
        return [Task.from_dict(obj) for obj in tasks]

    get_tasks_async = async_wrap(get_tasks)

    def add_task(self, content: str, **kwargs) -> Task:
        endpoint = get_rest_url(TASKS_ENDPOINT)
        data: Dict[str, Any] = {"content": content}
        data.update(kwargs)
        task = post(self._session, self._token, endpoint, data=data)
        return Task.from_dict(task)

    add_task_async = async_wrap(add_task)

    def update_task(self, task_id: str, **kwargs) -> Task:
        endpoint = get_rest_url(f"{TASKS_ENDPOINT}/{task_id}")
        task = post(self._session, self._token, endpoint, data=kwargs)
        return Task.from_dict(task)

    update_task_async = async_wrap(update_task)

    def close_task(self, task_id: str, **kwargs) -> bool:
        endpoint = get_rest_url(f"{TASKS_ENDPOINT}/{task_id}/close")
        success = post(self._session, self._token, endpoint, data=kwargs)
        return success

    close_task_async = async_wrap(close_task)

    def reopen_task(self, task_id: str, **kwargs) -> bool:
        endpoint = get_rest_url(f"{TASKS_ENDPOINT}/{task_id}/reopen")
        success = post(self._session, self._token, endpoint, data=kwargs)
        return success

    reopen_task_async = async_wrap(reopen_task)

    def delete_task(self, task_id: str, **kwargs) -> bool:
        endpoint = get_rest_url(f"{TASKS_ENDPOINT}/{task_id}")
        success = delete(self._session, self._token, endpoint, args=kwargs)
        return success

    delete_task_async = async_wrap(delete_task)
