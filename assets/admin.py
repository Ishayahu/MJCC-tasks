from django.contrib import admin
from assets.models import Asset, Payment, Cash, Cashless, Contractor, Garanty, Asset_type, Status, Budget, Repair, Place_Asset, Place, Cartridge, Cartridge_Model_General_Model, Cartridge_General_Model_Printer_Model, Cartridge_Printer, ROM, Cooler, Storage, Acoustics, Telephone, Battery, Optical_Drive, Printer, Power_suply, Motherboard, CPU, Case

admin.site.register(Asset)
admin.site.register(Payment)
admin.site.register(Cash)
admin.site.register(Cashless)
admin.site.register(Contractor)
admin.site.register(Garanty)
admin.site.register(Asset_type)
admin.site.register(Status)
admin.site.register(Budget)
admin.site.register(Repair)
admin.site.register(Place_Asset)
admin.site.register(Place)
admin.site.register(Cartridge)
admin.site.register(Cartridge_Model_General_Model)
admin.site.register(Cartridge_General_Model_Printer_Model)
admin.site.register(Cartridge_Printer)
admin.site.register(ROM)
admin.site.register(Cooler)
admin.site.register(Storage)
admin.site.register(Acoustics)
admin.site.register(Telephone)
admin.site.register(Battery)
admin.site.register(Optical_Drive)
admin.site.register(Printer)
admin.site.register(Power_suply)
admin.site.register(Motherboard)
admin.site.register(CPU)
admin.site.register(Case)

#class WorkerAdmin(admin.ModelAdmin):
    #list_display = ('fio','login','tel','mail','raiting')
#class ClientAdmin(admin.ModelAdmin):
    #list_display = ('fio','login','tel','mail','raiting')


#class TaskAdmin(admin.ModelAdmin):
    #search_fields = ('name', 'description', 'client', 'category', 'worker')
    #list_filter = ('client', 'start_date', 'due_date', 'done_date', 'priority', 'category', 'worker', 'pbw', 'pbu')
    #date_hierarchy = 'due_date'
    #ordering = ('-due_date', '-priority','worker')
#class RegularTaskAdmin(admin.ModelAdmin):
    #search_fields = ('name', 'description', 'client', 'category', 'worker')
    #list_filter = ('client', 'start_date', 'next_date', 'when_to_reminder','stop_date', 'priority', 'category', 'worker', 'period')
    #date_hierarchy = 'next_date'
    #ordering = ('next_date', '-priority','worker')

#admin.site.register(Note)
#admin.site.register(Resource)
#admin.site.register(File)
#admin.site.register(Person, WorkerAdmin)
#admin.site.register(ProblemByUser)
#admin.site.register(ProblemByWorker)
#admin.site.register(Categories)
#admin.site.register(Task, TaskAdmin)
#admin.site.register(RegularTask, RegularTaskAdmin)
#admin.site.register(Joker)
#admin.site.register(Joker_Visit)
