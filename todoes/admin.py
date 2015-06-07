from django.contrib import admin
from todoes.models import Note, Resource, File, Task, ProblemByWorker, ProblemByUser, Categories, Joker, Joker_Visit, Person, RegularTask

class WorkerAdmin(admin.ModelAdmin):
    list_display = ('fio','login','tel','mail','raiting')
class ClientAdmin(admin.ModelAdmin):
    list_display = ('fio','login','tel','mail','raiting')


class TaskAdmin(admin.ModelAdmin):
    search_fields = ('id','name', 'description', )
    list_filter = ('client', 'start_date', 'due_date', 'done_date', 'priority', 'category', 'worker', 'pbw', 'pbu')
    date_hierarchy = 'due_date'
    ordering = ('-due_date', '-priority','worker')
class RegularTaskAdmin(admin.ModelAdmin):
    search_fields = ('name', 'description', 'client', 'category', 'worker')
    list_filter = ('client', 'start_date', 'next_date', 'when_to_reminder','stop_date', 'priority', 'category', 'worker', 'period')
    date_hierarchy = 'next_date'
    ordering = ('next_date', '-priority','worker')

admin.site.register(Note)
admin.site.register(Resource)
admin.site.register(File)
admin.site.register(Person, WorkerAdmin)
admin.site.register(ProblemByUser)
admin.site.register(ProblemByWorker)
admin.site.register(Categories)
admin.site.register(Task, TaskAdmin)
admin.site.register(RegularTask, RegularTaskAdmin)
admin.site.register(Joker)
admin.site.register(Joker_Visit)
