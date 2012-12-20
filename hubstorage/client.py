"""
High level Hubstorage client
"""
import requests
from .utils import xauth
from .project import Project
from .job import Job
from .batchuploader import BatchUploader


class HSClient(object):

    DEFAULT_ENDPOINT = 'http://storage.scrapinghub.com:8002'

    def __init__(self, auth=None, endpoint=None):
        self.auth = xauth(auth)
        self.endpoint = endpoint or self.DEFAULT_ENDPOINT
        self.session = requests.session()
        self._bu = None

    @property
    def bu(self):
        if self._bu is None:
            self._bu = BatchUploader(self)
        return self._bu

    def get_job(self, *args, **kwargs):
        return Job(self, *args, **kwargs)

    def new_job(self, projectid, *args, **jobparams):
        project = self.get_project(projectid)
        return project.new_job(*args, **jobparams)

    def get_project(self, *args, **kwargs):
        return Project(self, *args, **kwargs)

    def close(self):
        if self._bu:
            self._bu.close()
