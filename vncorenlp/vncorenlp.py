#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import os
import subprocess
import time

import requests
from requests.exceptions import RequestException

__author__ = 'dnanhkhoa'

VNCORENLP_SERVER = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                 '../bin/VnCoreNLPServer.jar'))


class VnCoreNLP(object):
    def __init__(self, address='0.0.0.0', port=None, annotators='wseg,pos,ner,parse', timeout=30, quiet=True):
        self.logger = logging.getLogger(__name__)

        self.annotators = annotators
        self.url = None
        self.timeout = timeout

        # Check if server file exists
        if not os.path.isfile(VNCORENLP_SERVER):
            raise FileNotFoundError('File "VnCoreNLPServer.jar" was not found, please re-install this package.')

        # Check if Java exists
        if subprocess.call(['java', '-version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True):
            raise FileNotFoundError('Java was not found, please install JRE or JDK 1.8 first.')

        args = ['java', '-Xmx2g', '-jar', VNCORENLP_SERVER]

        # Start server
        self.process = None  # subprocess.Popen(args)

        # Waiting until the server is available
        while not self.is_alive():
            break
            self.logger.info('Waiting until the server is available.')
            time.sleep(5)
        self.logger.info('The server is available.')

    def close(self):
        # Stop server and clean up
        if self.process:
            self.logger.info(__class__.__name__ + ': cleaning up...')
            self.logger.info(__class__.__name__ + ': killing VnCoreNLPServer process (%s)...' % self.process.pid)

            # Kill process
            self.process.kill()
            self.process = None

            self.logger.info(__class__.__name__ + ': done.')

    def is_alive(self):
        # Check if server is alive
        try:
            response = requests.get(url=self.url, timeout=self.timeout)
            response.raise_for_status()
            return response.status_code == requests.codes.ok
        except RequestException as e:
            self.logger.exception(e)
        return False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def annotate(self, text, annotators=None):
        if annotators:
            pass
        else:
            annotators = self.annotators

        data = {
            'text': text.encode('UTF-8'),
            'props': annotators
        }
        response = requests.post(url=self.url + '/handle', data=data, timeout=self.timeout)
        response.raise_for_status()
        response = response.json()
        # status:bool
        return response.get('result', None)

    def tokenize(self, text):
        annotated_text = self.annotate(text=text)

    def pos_tag(self, text):
        pass

    def ner(self, text):
        pass

    def dep_parse(self, text):
        pass

    def detect_language(self, text):
        pass
