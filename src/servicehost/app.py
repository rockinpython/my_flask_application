import logging
from src.servicehost.appsetup.new_flask_app import application
from src.servicehost.settings import AppSettings
logger = logging.getLogger(__name__)

app = application

def main():
    logger.info('task api started')
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()