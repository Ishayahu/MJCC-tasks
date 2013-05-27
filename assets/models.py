# -*- coding:utf-8 -*-
# coding=<utf8>

from django.db import models

# Модели для подключения активов

class Asset(models.Model):
    asset_type = models.ForeignKey('Asset_type')
    payment = models.ForeignKey('Payment')
    date_of_write_off = models.DateTimeField()
    garanty = models.ForeignKey('Garanty')
    current_place = models.ForeignKey('Place_Asset')
    model = models.CharField(max_length=140)
    status = models.ForeignKey('Status')
    claim = models.ForeignKey('Claim')
    guarantee_period = models.IntegerField()
    note = models.TextField()
class Payment(models.Model):
    cash = models.ForeignKey('Cash')
    cashless = models.ForeignKey('Cashless')
class Cash(models.Model):
    date = models.DateTimeField()
    price = models.DecimalField(decimal_places=2, max_digits=8)
    contractor = models.ForeignKey('Contractor')
class Cashless(models.Model):
    date_of_invoice = models.DateTimeField()
    dates = models.TextField()
    stages = models.TextField()
    date_of_assets = models.DateTimeField()
    date_of_documents = models.DateTimeField()
    price = models.DecimalField(decimal_places=2, max_digits=8)
    contractor = models.ForeignKey('Contractor')
class Contractor(models.Model):
    name = models.CharField(max_length=140)
    tel = models.CharField(max_length=10,blank = True, null = True)
    email = models.EmailField(blank = True, null = True)
    tel_of_support = models.CharField(max_length=10,blank = True, null = True) 
    contact_name = models.CharField(max_length=140)
class Garanty(models.Model):
    number = models.IntegerField() 
class Asset_type(models.Model):
    asset_type = models.CharField(max_length=200)
class Status(models.Model):
    status = models.CharField(max_length=100)
class Budget(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()
class Repair(models.Model):
    date_of_failure = models.DateTimeField()
    failure = models.TextField()
    repair = models.TextField()
    date_repair_start = models.DateTimeField()
    date_repair_end = models.DateTimeField()
    payment = models.ForeignKey('Payment')
    date_of_write_off = models.DateTimeField()
    garanty = models.ForeignKey('Garanty')    
    guarantee_period = models.IntegerField()
    asset = models.ForeignKey('Asset')
class Place_Asset(models.Model):
    installation_date = models.DateTimeField()
    drawdown_date = models.DateTimeField()
    asset = models.ForeignKey('Asset')
    place = models.ForeignKey('Place')
    reason_of_drawdown = modes.TextField()
class Place(models.Model):
    place = models.CharField(max_length=140)
class Cartridge(models.Model):
    model = models.CharField(max_length=140)
    payment = models.ForeignKey('Payment')
    status = models.ForeignKey('Status')
class Cartridge_Model_General_Model(models.Model):
    model = models.CharField(max_length=140)
    general_model = models.CharField(max_length=140)
class Cartridge_General_Model_Printer_Model(models.Model):
    printer_model = models.CharField(max_length=140)
    general_model = models.CharField(max_length=140)
class Cartridge_Printer(model.Models):
    installation_date = models.DateTimeField()
    drawdown_date = models.DateTimeField()
    cartridge = models.ForeignKey('Cartridge')
    printer = models.ForeignKey('Asset')
    
# Таблицы справочников моделей по типам
# Все варианты выбора, такие как производители, форм-факторы памяти и т.д. хранятся в catalogue.py
import catalogue
class ROM(models.Model):
    firm = models.CharField(max_length=50, choises = catalogue.ROM_firms)
    rom_type = models.CharField(max_length=50, choises = catalogue.ROM_type)
    form_factor = models.CharField(max_length=50, choises = catalogue.ROM_form_factors)
    v = models.CharField(max_length=50, choises = catalogue.ROM_V)
    clock_ferquency = models.CharField(max_length=50, choises = catalogue.ROM_clock_frequency)
    throughput = models.CharField(max_length=50, choises = catalogue.ROM_throughput)
    low_profile = models.BooleanField(default=False)
    radiator = models.BooleanField(default=False)
class Cooler(models.Model):
    firm = models.CharField(max_length=50, choises = catalogue.Cooler_firms)
    destination = models.CharField(max_length=50, choises = catalogue.Cooler_destination)
    sockets = models.TextField(blank = True, null = True)
    number_of_fans = models.IntegerField()
    diametr_of_fans = models.IntegerField()
    type_of_connector = models.CharField(max_length=10, choises = catalogue.Cooler_connector)
    rpm = models.CharField(max_length=12)
    cfm = models.CharField(max_length=15)
    noise  = models.CharField(max_length=20)
class Storage(models.Model):
    firm = models.CharField(max_length=50, choises = catalogue.Storage_firms)
    form_factor = models.CharField(max_length=10, choises = catalogue.Storage_form_factor)
    volume = models.IntegerField()
    interfaces = models.TextField(blank = True, null = True)
    rpm = models.CharField(max_length=20, choises = catalogue.Storage_rpm)
    # В Mb/сек
    v_read = models.IntegerField()
    v_write = models.IntegerField()
class Acoustics(models.Model):
    firm = models.CharField(max_length=50, choises = catalogue.Acoustics_firms)
    acoustics_type = models.CharField(max_length=10, choises = catalogue.Acoustics_type)
    # Суммарная мощность в ваттах
    rms = models.IntegerField()
    power_form_usb = models.BooleanField(default=False)
    power_from_circuit = models.BooleanField(default=False)
    power_from_battary = models.BooleanField(default=False)
    remote_control = models.BooleanField(default=False)
    frequency_interval = models.CharField(max_length=20)
    headphone_jack = models.BooleanField(default=False)
    # В децебелах
    signal_noise_ratio = models.CharField(max_length=20)
class Telephone(models.Model):
    firm = models.CharField(max_length=50, choises = catalogue.Telephone_firms)
    aon = models.BooleanField(default=False)
    display = models.BooleanField(default=False)
    tel_book = models.BooleanField(default=False)
    clock = models.BooleanField(default=False)
    alarm_clock = models.BooleanField(default=False)
    speakerphone = models.BooleanField(default=False)
    frequency = models.CharField(max_length=20, choises = catalogue.Telephone_frequency)
    DECT = models.BooleanField(default=False)
    GAP = models.BooleanField(default=False)
    headset = models.BooleanField(default=False)
class Battery(models.Model):
    firm = models.CharField(max_length=50, choises = catalogue.Battery_firms)
    battery_type = models.CharField(max_length=10, choises = catalogue.Battery_type)
    rechargeable = models.BooleanField(default=False)
class Optical_Drive(models.Model):
    firm = models.CharField(max_length=50, choises = catalogue.Optical_Drive_firms)
    optical_drive_type = models.CharField(max_length=10, choises = catalogue.Optical_drive_type)
    interface = models.CharField(max_length=20, choises = catalogue.Optical_Drive_interfaces)
class Network_equipment(models.Model):
    firm = models.CharField(max_length=50, choises = catalogue.Network_equipment_firms)
    firm = models.CharField(max_length=15, choises = catalogue.Network_equipment_type)
    # Можно устанавливать в стойку
    rackable = models.BooleanField(default=False)
    dhcp_server = models.BooleanField(default=False)
    firewall = models.BooleanField(default=False)
    nat = models.BooleanField(default=False)
    vpn = models.BooleanField(default=False)
    ipv6_ready = models.BooleanField(default=False)
    WiFi= models.CharField(max_length=20, choises = catalogue.Network_equipment_WiFi_type)    
    SNMP = models.BooleanField(default=False)
    Web = models.BooleanField(default=False)
    Telnet = models.BooleanField(default=False)
    Serial = models.BooleanField(default=False)
class Printer(models.Model):
    network
    firm
    color
    v_print
    
    
"""
    def __unicode__(self):
        return u";".join((str(self.id),self.name,"\t"+self.worker.fio))
    class Meta:
        ordering = ['priority','due_date']
"""