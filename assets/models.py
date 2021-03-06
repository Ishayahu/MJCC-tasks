# -*- coding:utf-8 -*-
# coding=<utf8>

from django.db import models
##from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext as _
# Модели для подключения активов

class Asset(models.Model):
    asset_type = models.ForeignKey('Asset_type')
    payment = models.ForeignKey('Payment')
    date_of_write_off = models.DateTimeField(blank=True, null=True)
    garanty = models.ForeignKey('Garanty')
    # current_place = models.ForeignKey('Place_Asset',related_name='for_asset')
    model = models.CharField(max_length=140)
    status = models.ForeignKey('Status')
    # claim = models.ForeignKey('Claim',blank=True, null=True)
    guarantee_period = models.IntegerField()
    note = models.TextField(blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=8)
    def __unicode__(self):
        return u';'.join((str(self.id),self.asset_type.asset_type,self.model,self.status.status))
# Оплата - либо нал, либо безнал, либо то и то
class Payment(models.Model):
    cash = models.ForeignKey('Cash',blank=True, null=True)
    cashless = models.ForeignKey('Cashless',blank=True, null=True)
    deleted = models.BooleanField(default=False)
    def __unicode__(self):
        if not self.cash:
            return u';'.join((str(self.id),u"CASHLESS:"+self.cashless.__unicode__()))
        if not self.cashless:
            return u';'.join((str(self.id),u"CASH:"+self.cash.__unicode__()))
        return u';'.join((str(self.id),u"CASH:"+self.cash.__unicode__(),u"CASHLESS:"+self.cashless.__unicode__()))

# Чек/Остатки - то, что за нал
class Cash(models.Model):
    date = models.DateTimeField()
    contractor = models.ForeignKey('Contractor')
    bill_number =  models.CharField(max_length=40)
    closed_for = models.TextField(blank = True, null = True)
    def __unicode__(self):
        return u';'.join((str(self.id),self.bill_number,str(self.date),self.contractor.name))
# Счёт по безналу
class Cashless(models.Model):
    date_of_invoice = models.DateTimeField()
    dates = models.TextField(blank = True, null = True) # даты прохождения этапов, разделённые ;
    stages = models.TextField() # этапы прохождения счёта, разделённые ;
    date_of_assets = models.DateTimeField(blank = True, null = True)
    date_of_documents = models.DateTimeField(blank = True, null = True)
    contractor = models.ForeignKey('Contractor')
    bill_number =  models.CharField(max_length=40)
    def __unicode__(self):
        return u';'.join((str(self.id),self.bill_number,self.contractor.name,self.stages))
# Заявка
class Claim(models.Model):
    date_of_invoice = models.DateTimeField()
    dates = models.TextField()
    stages = models.TextField()
    date_of_assets = models.DateTimeField()
    date_of_documents = models.DateTimeField()
    # Сколько денег дано по заявке
    price = models.DecimalField(decimal_places=2, max_digits=8)
    contractor = models.ForeignKey('Contractor')
class Contractor(models.Model):
    name = models.CharField(max_length=140)
    tel = models.CharField(max_length=10,blank = True, null = True)
    email = models.EmailField(blank = True, null = True)
    tel_of_support = models.CharField(max_length=10,blank = True, null = True)
    contact_name = models.CharField(max_length=140)
    def __unicode__(self):
        return u';'.join((str(self.id),self.name,self.contact_name))
class Garanty(models.Model):
    number = models.IntegerField()
    def __unicode__(self):
        return u';'.join((str(self.id),str(self.number)))
class Asset_type(models.Model):
    asset_type = models.CharField(max_length=200)
    catalogue_name = models.CharField(max_length=30)
    def __unicode__(self):
        return u';'.join((str(self.id),self.asset_type,self.catalogue_name))
class Status(models.Model):
    status = models.CharField(max_length=100)
    def __unicode__(self):
        return str(self.id)+';'+self.status
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
    drawdown_date = models.DateTimeField(blank = True, null = True)
    asset = models.ForeignKey('Asset')
    place = models.ForeignKey('Place')
    reason_of_drawdown = models.TextField(blank = True, null = True)
    def __unicode__(self):
        # a = str(self.id)
        # b = unicode(self.asset.model)
        # c = self.place.place
        # d = str(self.installation_date)
        return u';'.join((str(self.id),unicode(self.asset.model),unicode(self.place.place),str(self.installation_date),str(self.drawdown_date)))
class Place(models.Model):
    place = models.CharField(max_length=140)
    def __unicode__(self):
        return str(self.id)+';'+self.place
class Cartridge(models.Model):
    model = models.CharField(max_length=140)
    payment = models.ForeignKey('Payment')
    status = models.ForeignKey('Status')
class Cartridge_Model_General_Model(models.Model):
    model = models.CharField(max_length=140)      # общая
    model_name = models.CharField(max_length=140) # частная
class Cartridge_General_Model_Printer_Model(models.Model):
    printer_model = models.CharField(max_length=140)
    cartrige_model = models.CharField(max_length=140)
class Cartridge_Printer(models.Model):
    installation_date = models.DateTimeField()
    drawdown_date = models.DateTimeField()
    cartridge = models.ForeignKey('Cartridge')
    printer = models.ForeignKey('Asset')

# Таблицы справочников моделей по типам
# Все варианты выбора, такие как производители, форм-факторы памяти и т.д. хранятся в catalogue.py
import catalogue
class ROM(models.Model):
    model_name = models.CharField(max_length=50)
    firm = models.CharField(max_length=50, choices = catalogue.ROM_firms)
    rom_type = models.CharField(max_length=50, choices = catalogue.ROM_type)
    form_factor = models.CharField(max_length=50, choices = catalogue.ROM_form_factors)
    v = models.CharField(max_length=50, choices = catalogue.ROM_V)
    clock_ferquency = models.CharField(max_length=50, choices = catalogue.ROM_clock_frequency)
    throughput = models.CharField(max_length=50, choices = catalogue.ROM_throughput)
    low_profile = models.BooleanField(default=False)
    radiator = models.BooleanField(default=False)
class Cooler(models.Model):
    model_name = models.CharField(max_length=50)
    firm = models.CharField(max_length=50, choices = catalogue.Cooler_firms)
    destination = models.CharField(max_length=50, choices = catalogue.Cooler_destination)
    sockets = models.TextField(blank = True, null = True)
    number_of_fans = models.IntegerField()
    diametr_of_fans = models.IntegerField()
    type_of_connector = models.CharField(max_length=10, choices = catalogue.Cooler_connector)
    rpm = models.CharField(max_length=12)
    cfm = models.CharField(max_length=15)
    noise  = models.CharField(max_length=20)
class Storage(models.Model):
    model_name = models.CharField(max_length=50)
    firm = models.CharField(max_length=50, choices = catalogue.Storage_firms)
    form_factor = models.CharField(max_length=10, choices = catalogue.Storage_form_factor)
    volume = models.IntegerField()
    interfaces = models.TextField(blank = True, null = True) #?
    rpm = models.CharField(max_length=20, choices = catalogue.Storage_rpm)

    # TODO: добавить кеш
    # В Mb/сек
    v_read = models.IntegerField()
    v_write = models.IntegerField()
class Acoustics(models.Model):
    model_name = models.CharField(max_length=50)
    firm = models.CharField(max_length=50, choices = catalogue.Acoustics_firms)
    acoustics_type = models.CharField(max_length=10, choices = catalogue.Acoustics_type)
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
    model_name = models.CharField(max_length=50)
    firm = models.CharField(max_length=50, choices = catalogue.Telephone_firms)
    aon = models.BooleanField(default=False)
    display = models.BooleanField(default=False)
    tel_book = models.BooleanField(default=False)
    clock = models.BooleanField(default=False)
    alarm_clock = models.BooleanField(default=False)
    speakerphone = models.BooleanField(default=False)
    frequency = models.CharField(max_length=20, choices = catalogue.Telephone_frequency)
    DECT = models.BooleanField(default=False)
    GAP = models.BooleanField(default=False)
    headset = models.BooleanField(default=False)
class Battery(models.Model):
    model_name = models.CharField(max_length=50)
    firm = models.CharField(max_length=50, choices = catalogue.Battery_firms)
    battery_type = models.CharField(max_length=10, choices = catalogue.Battery_type)
    rechargeable = models.BooleanField(default=False)
class Optical_Drive(models.Model):
    model_name = models.CharField(max_length=50)
    firm = models.CharField(max_length=50, choices = catalogue.Optical_Drive_firms)
    optical_drive_type = models.CharField(max_length=10, choices = catalogue.Optical_Drive_type)
    interface = models.CharField(max_length=20, choices = catalogue.Optical_Drive_interfaces)
class Network_equipment(models.Model):
    model_name = models.CharField(max_length=50)
    firm = models.CharField(max_length=50, choices = catalogue.Network_equipment_firms)
    equipment_type = models.CharField(max_length=15, choices = catalogue.Network_equipment_type)
    # Можно устанавливать в стойку
    rackable = models.BooleanField(default=False)
    dhcp_server = models.BooleanField(default=False)
    firewall = models.BooleanField(default=False)
    nat = models.BooleanField(default=False)
    vpn = models.BooleanField(default=False)
    ipv6_ready = models.BooleanField(default=False)
    WiFi = models.CharField(max_length=20, choices = catalogue.Network_equipment_WiFi_type)
    SNMP = models.BooleanField(default=False)
    Web = models.BooleanField(default=False)
    Telnet = models.BooleanField(default=False)
    Serial = models.BooleanField(default=False)
class Printer(models.Model):
    model_name = models.CharField(max_length=50,verbose_name=_("Model name"))
    wifi = models.BooleanField(default=False,verbose_name=_("WiFi connection"))
    ethernet = models.BooleanField(default=False,verbose_name=_("Ethernet connection"))
    lazer = models.BooleanField(default=True,verbose_name=_("Laser printing"))
    firm = models.CharField(max_length=20, choices = catalogue.Printer_firm,verbose_name=_("Firm"))
    color = models.BooleanField(default=False,verbose_name=_("Colored?"))
    v_mono_print = models.IntegerField(verbose_name=_("Monochrome printing speed"))
    v_color_print = models.IntegerField(blank = True, null = True,verbose_name=_("Color printing speed"))
    def __unicode__(self):
        return str(self.id)+';'+self.firm+" "+self.model_name+";color="+str(self.color)+";ethernet="+str(self.ethernet)+";wifi="+str(self.wifi)+";v="+str(self.v_mono_print)+";vc="+str(self.v_color_print)
class Power_suply(models.Model):
    model_name = models.CharField(max_length=50)
    firm = models.CharField(max_length=20, choices = catalogue.Power_suply_firm)
    power = models.IntegerField()
    modular = models.BooleanField(default=False)
    performance = models.DecimalField(max_digits=4,decimal_places=2)
    ATX_version = models.CharField(max_length=10, choices = catalogue.Power_ATX_version)
    number_of_sata = models.DecimalField(max_digits=1,decimal_places=0)
    number_of_molex = models.DecimalField(max_digits=1,decimal_places=0)
class UPS(models.Model):
    """
    модель
    производитель
    количество комп. разъёмов с батареей
    количество комп. разъёмов без батареи
    количество розеток с батарей
    количество розеток без батареи
    защита телефонии
    защита rj-45
    выходная мощность
    время работы
    RS-232
    USB
    ethernet
    LCD-дисплей
    вес
    тип
    """
    model_name = models.CharField(max_length=50)
    firm = models.CharField(max_length=30, choices = catalogue.UPS_firm)
    number_of_comp_connectors_with_batt = models.IntegerField()
    number_of_comp_connectors_without_batt = models.IntegerField()
    number_of_outlets_with_batt = models.IntegerField()
    number_of_outlets_without_batt = models.IntegerField()
    telephone_line_protection = models.BooleanField(default=False)
    lan_protection = models.BooleanField(default=False)
    output_power = models.IntegerField()
    working_time = models.DecimalField(max_digits=4,decimal_places=2)
    rs232_interface = models.BooleanField(default=False)
    usb_interface = models.BooleanField(default=False)
    ethernet_interface = models.BooleanField(default=False)
    lcd_display = models.BooleanField(default=False)
    weight = models.DecimalField(max_digits=4,decimal_places=2)
    type = models.CharField(max_length=30, choices = catalogue.UPS_types)
class Delivery(models.Model):
    model_name = models.CharField(max_length=50)
# class Delivery(models.Model):
#     model_name = models.CharField(max_length=50)
class Motherboard(models.Model):
    model_name = models.CharField(max_length=50, verbose_name=_("Model name"))
    firm = models.CharField(max_length=20, choices = catalogue.Motherboard_firm)
    socket = models.CharField(max_length=20, choices = catalogue.Sockets)
    chipset = models.CharField(max_length=20, choices = catalogue.Motherboard_chipset)
    EFI = models.BooleanField(default=False)
    rom_type = models.CharField(max_length=20, choices = catalogue.Motherboard_rom_types)
    rom_number = models.IntegerField()
    rom_max_value = models.IntegerField()
    rom_frequency = models.CharField(max_length=50)
    FSB  = models.CharField(max_length=50, blank = True, null = True)
    FDD = models.IntegerField()
    IDE = models.IntegerField()
    COM = models.IntegerField()
    USB2 = models.IntegerField()
    USB3 = models.IntegerField()
    PCI_E_number = models.IntegerField()
    PCI_E_type = models.CharField(max_length=10, choices = catalogue.Motherboard_pci_e_types)
    graphics = models.CharField(max_length=10, choices = catalogue.Motherboard_integrated_graphics)
    form_factor = models.CharField(max_length=10, choices = catalogue.Motherboard_form_factor)
    HDMI = models.BooleanField(default=False)
    SLI = models.BooleanField(default=False)
    CrossFire = models.BooleanField(default=False)
    eSATA = models.IntegerField()
    SATA_RAID = models.CharField(max_length=15)
    Ethernet = models.CharField(max_length=20, choices = catalogue.Ethernet_types)
    Ethernet_number = models.IntegerField()
    WiFi = models.CharField(max_length=20, choices = catalogue.WiFi_types)
    Bluetooth = models.BooleanField(default=False)
    Audio = models.CharField(max_length=10, choices = catalogue.Motherboard_audio)
    FireWire = models.IntegerField()
    LPT = models.IntegerField()
    PS_2 = models.IntegerField()
    DisplayPort = models.IntegerField()
    SupportedROM = models.TextField(blank = True, null = True)
    SupportedCPU = models.TextField(blank = True, null = True)
class CPU(models.Model):
    model_name = models.CharField(max_length=50)
    firm = models.CharField(max_length=20, choices = catalogue.CPU_firm)
    socket = models.CharField(max_length=20, choices = catalogue.Sockets)
    frequency = models.CharField(max_length=20)
    core = models.CharField(max_length=20, choices = catalogue.CPU_core)
    L1 = models.CharField(max_length=20, choices = catalogue.CPU_L1)
    L2 = models.CharField(max_length=20, choices = catalogue.CPU_L2)
    L3 = models.CharField(max_length=20, choices = catalogue.CPU_L3)
    technology = models.CharField(max_length=20, choices = catalogue.CPU_technology)
    core_number = models.IntegerField()
    VT = models.BooleanField(default=False)
    integrated_graphics = models.BooleanField(default=False)
    # TODO: добавить описание графики
    TPD = models.CharField(max_length=20)
class Case(models.Model):
    model_name = models.CharField(max_length=50)
    firm = models.CharField(max_length=20, choices = catalogue.Case_firm)
    form_factor = models.CharField(max_length=20, choices = catalogue.Case_form_factor)
    supported_mb_types = models.TextField()
    place_of_power_suply = models.CharField(max_length=20, choices = catalogue.Case_power_suply_place)
    usb_fp = models.IntegerField()
    audio_fp = models.IntegerField()
    eSATA_fp = models.IntegerField()
    eSATA_rp = models.IntegerField()
    FireWire_fp = models.IntegerField()
    FireWire_rp = models.IntegerField()
    number_of_35 = models.IntegerField()
    number_of_525 = models.IntegerField()
    water_ready = models.BooleanField(default=False)
    number_of_extension_slot = models.IntegerField()
    number_of_fan_places = models.IntegerField()
    size = models.CharField(max_length=50)

class CKC(models.Model):
    model_name = models.CharField(max_length=150,verbose_name=_("Model name"))
    def __unicode__(self):
        return str(self.id)+';'+self.model_name
class Telephone_Works(models.Model):
    model_name = models.CharField(max_length=150,verbose_name=_("Model name"))
    def __unicode__(self):
        return str(self.id)+';'+self.model_name



"""
    def __unicode__(self):
        return u";".join((str(self.id),self.name,"\t"+self.worker.fio))
    class Meta:
        ordering = ['priority','due_date']
"""