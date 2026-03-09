from django.apps import AppConfig


# class DevasappConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'DevasAPP'



class DevasappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'DevasAPP'

    def ready(self):
        import DevasAPP.signals