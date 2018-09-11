from src.controllers.tasks import taskController


class RoutesRegistration:
    def register_in_app(self, app):
        app.register_blueprint(taskController)

        return app