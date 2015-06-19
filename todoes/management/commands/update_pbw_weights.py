from django.core.management.base import BaseCommand, CommandError
# from todoes.models import Note, Task, RegularTask, ProblemByWorker
from todoes.utils import update_weigth

class Command(BaseCommand):
    help = 'Updates pbw weights'

    def handle(self, *args, **options):
        update_weigth()