import os
import json
import yaml
import logging.config
import uuid

from boto3.session import Session
from pkg_resources import resource_listdir, resource_string

from src.servicehost import __name__ as pkg_name


class AppSettings(object):
    PREFIX = 'POC_'

    def __init__(self):
        self._load_environment_configs()
        self._load_local_settings()
        print(self.logging_json)

    def _load_environment_configs(self):
        self.env = {var.replace(self.PREFIX, '').lower(): val
                    for var, val in os.environ.items()
                    if var.startswith(self.PREFIX)}

    def _load_local_settings(self):
        for f in resource_listdir(pkg_name, 'appsettings'):
            # Only json and yml is supported now. If you want something more
            # fancy, add the import and the condition here.
            if not f.endswith('.json') and not f.endswith('.yml'):
                continue

            resource = resource_string(pkg_name, 'appsettings/{}'.format(f)).decode('utf-8')
            if f.endswith('.json'):
                config = json.loads(resource)
            else:
                loaded = yaml.load(resource)
                config = loaded['logging']

            name = os.path.splitext(os.path.basename(f))[0]

            if name != 'logging':
                setattr(self, name, config)

            else:
                if 'fluent' in config['handlers']:
                    if 'log_fluent_host' in self.env:
                        config['handlers']['fluent']['host'] = self.env['log_fluent_host']
                    if 'log_fluent_port' in self.env:
                        config['handlers']['fluent']['port'] = int(self.env['log_fluent_port'])

                if 'watchtower' in config['handlers']:
                    boto3_session = Session(aws_access_key_id=self.env['aws_key_id'],
                                            aws_secret_access_key=self.env['aws_secret'],
                                            region_name=self.env['aws_region'])

                    watchtower_handler = config['handlers']['watchtower']
                    watchtower_handler['boto3_session'] = boto3_session
                    watchtower_handler['log_group'] = watchtower_handler['log_group'].format(**self.env)
                    watchtower_handler['stream_name'] = str(uuid.uuid4())

                logging.config.dictConfig(config)
                logging.getLogger().setLevel(self.env.get('log_level', 'INFO'))


config = AppSettings()
