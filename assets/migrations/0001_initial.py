# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Asset'
        db.create_table('assets_asset', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('asset_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['assets.Asset_type'])),
            ('payment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['assets.Payment'])),
            ('date_of_write_off', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('garanty', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['assets.Garanty'])),
            ('current_place', self.gf('django.db.models.fields.related.ForeignKey')(related_name='for_asset', to=orm['assets.Place_Asset'])),
            ('model', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('status', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['assets.Status'])),
            ('claim', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['assets.Claim'])),
            ('guarantee_period', self.gf('django.db.models.fields.IntegerField')()),
            ('note', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('assets', ['Asset'])

        # Adding model 'Payment'
        db.create_table('assets_payment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cash', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['assets.Cash'])),
            ('cashless', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['assets.Cashless'])),
        ))
        db.send_create_signal('assets', ['Payment'])

        # Adding model 'Cash'
        db.create_table('assets_cash', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
            ('contractor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['assets.Contractor'])),
        ))
        db.send_create_signal('assets', ['Cash'])

        # Adding model 'Cashless'
        db.create_table('assets_cashless', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_of_invoice', self.gf('django.db.models.fields.DateTimeField')()),
            ('dates', self.gf('django.db.models.fields.TextField')()),
            ('stages', self.gf('django.db.models.fields.TextField')()),
            ('date_of_assets', self.gf('django.db.models.fields.DateTimeField')()),
            ('date_of_documents', self.gf('django.db.models.fields.DateTimeField')()),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
            ('contractor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['assets.Contractor'])),
        ))
        db.send_create_signal('assets', ['Cashless'])

        # Adding model 'Claim'
        db.create_table('assets_claim', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_of_invoice', self.gf('django.db.models.fields.DateTimeField')()),
            ('dates', self.gf('django.db.models.fields.TextField')()),
            ('stages', self.gf('django.db.models.fields.TextField')()),
            ('date_of_assets', self.gf('django.db.models.fields.DateTimeField')()),
            ('date_of_documents', self.gf('django.db.models.fields.DateTimeField')()),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
            ('contractor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['assets.Contractor'])),
        ))
        db.send_create_signal('assets', ['Claim'])

        # Adding model 'Contractor'
        db.create_table('assets_contractor', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('tel', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('tel_of_support', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('contact_name', self.gf('django.db.models.fields.CharField')(max_length=140)),
        ))
        db.send_create_signal('assets', ['Contractor'])

        # Adding model 'Garanty'
        db.create_table('assets_garanty', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('number', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('assets', ['Garanty'])

        # Adding model 'Asset_type'
        db.create_table('assets_asset_type', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('asset_type', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('catalogue_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('assets', ['Asset_type'])

        # Adding model 'Status'
        db.create_table('assets_status', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('assets', ['Status'])

        # Adding model 'Budget'
        db.create_table('assets_budget', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('start', self.gf('django.db.models.fields.DateTimeField')()),
            ('end', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('assets', ['Budget'])

        # Adding model 'Repair'
        db.create_table('assets_repair', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_of_failure', self.gf('django.db.models.fields.DateTimeField')()),
            ('failure', self.gf('django.db.models.fields.TextField')()),
            ('repair', self.gf('django.db.models.fields.TextField')()),
            ('date_repair_start', self.gf('django.db.models.fields.DateTimeField')()),
            ('date_repair_end', self.gf('django.db.models.fields.DateTimeField')()),
            ('payment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['assets.Payment'])),
            ('date_of_write_off', self.gf('django.db.models.fields.DateTimeField')()),
            ('garanty', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['assets.Garanty'])),
            ('guarantee_period', self.gf('django.db.models.fields.IntegerField')()),
            ('asset', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['assets.Asset'])),
        ))
        db.send_create_signal('assets', ['Repair'])

        # Adding model 'Place_Asset'
        db.create_table('assets_place_asset', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('installation_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('drawdown_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('asset', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['assets.Asset'])),
            ('place', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['assets.Place'])),
            ('reason_of_drawdown', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('assets', ['Place_Asset'])

        # Adding model 'Place'
        db.create_table('assets_place', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('place', self.gf('django.db.models.fields.CharField')(max_length=140)),
        ))
        db.send_create_signal('assets', ['Place'])

        # Adding model 'Cartridge'
        db.create_table('assets_cartridge', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('model', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('payment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['assets.Payment'])),
            ('status', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['assets.Status'])),
        ))
        db.send_create_signal('assets', ['Cartridge'])

        # Adding model 'Cartridge_Model_General_Model'
        db.create_table('assets_cartridge_model_general_model', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('model', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('general_model', self.gf('django.db.models.fields.CharField')(max_length=140)),
        ))
        db.send_create_signal('assets', ['Cartridge_Model_General_Model'])

        # Adding model 'Cartridge_General_Model_Printer_Model'
        db.create_table('assets_cartridge_general_model_printer_model', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('printer_model', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('general_model', self.gf('django.db.models.fields.CharField')(max_length=140)),
        ))
        db.send_create_signal('assets', ['Cartridge_General_Model_Printer_Model'])

        # Adding model 'Cartridge_Printer'
        db.create_table('assets_cartridge_printer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('installation_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('drawdown_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('cartridge', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['assets.Cartridge'])),
            ('printer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['assets.Asset'])),
        ))
        db.send_create_signal('assets', ['Cartridge_Printer'])

        # Adding model 'ROM'
        db.create_table('assets_rom', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('model_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('firm', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('rom_type', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('form_factor', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('v', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('clock_ferquency', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('throughput', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('low_profile', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('radiator', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('assets', ['ROM'])

        # Adding model 'Cooler'
        db.create_table('assets_cooler', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('model_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('firm', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('destination', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('sockets', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('number_of_fans', self.gf('django.db.models.fields.IntegerField')()),
            ('diametr_of_fans', self.gf('django.db.models.fields.IntegerField')()),
            ('type_of_connector', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('rpm', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('cfm', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('noise', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('assets', ['Cooler'])

        # Adding model 'Storage'
        db.create_table('assets_storage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('model_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('firm', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('form_factor', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('volume', self.gf('django.db.models.fields.IntegerField')()),
            ('interfaces', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('rpm', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('v_read', self.gf('django.db.models.fields.IntegerField')()),
            ('v_write', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('assets', ['Storage'])

        # Adding model 'Acoustics'
        db.create_table('assets_acoustics', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('model_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('firm', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('acoustics_type', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('rms', self.gf('django.db.models.fields.IntegerField')()),
            ('power_form_usb', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('power_from_circuit', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('power_from_battary', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('remote_control', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('frequency_interval', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('headphone_jack', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('signal_noise_ratio', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('assets', ['Acoustics'])

        # Adding model 'Telephone'
        db.create_table('assets_telephone', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('model_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('firm', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('aon', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('display', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('tel_book', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('clock', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('alarm_clock', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('speakerphone', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('frequency', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('DECT', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('GAP', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('headset', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('assets', ['Telephone'])

        # Adding model 'Battery'
        db.create_table('assets_battery', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('model_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('firm', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('battery_type', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('rechargeable', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('assets', ['Battery'])

        # Adding model 'Optical_Drive'
        db.create_table('assets_optical_drive', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('model_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('firm', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('optical_drive_type', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('interface', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('assets', ['Optical_Drive'])

        # Adding model 'Network_equipment'
        db.create_table('assets_network_equipment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('model_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('firm', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('equipment_type', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('rackable', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('dhcp_server', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('firewall', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('nat', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('vpn', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('ipv6_ready', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('WiFi', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('SNMP', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('Web', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('Telnet', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('Serial', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('assets', ['Network_equipment'])

        # Adding model 'Printer'
        db.create_table('assets_printer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('model_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('network', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('firm', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('color', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('v_print', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('assets', ['Printer'])

        # Adding model 'Power_suply'
        db.create_table('assets_power_suply', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('model_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('firm', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('power', self.gf('django.db.models.fields.IntegerField')()),
            ('modular', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('performance', self.gf('django.db.models.fields.DecimalField')(max_digits=4, decimal_places=2)),
            ('ATX_version', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('number_of_sata', self.gf('django.db.models.fields.DecimalField')(max_digits=1, decimal_places=0)),
            ('number_of_molex', self.gf('django.db.models.fields.DecimalField')(max_digits=1, decimal_places=0)),
        ))
        db.send_create_signal('assets', ['Power_suply'])

        # Adding model 'Motherboard'
        db.create_table('assets_motherboard', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('model_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('firm', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('socket', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('chipset', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('EFI', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('rom_type', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('rom_number', self.gf('django.db.models.fields.IntegerField')()),
            ('rom_max_value', self.gf('django.db.models.fields.IntegerField')()),
            ('rom_frequency', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('FSB', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('FDD', self.gf('django.db.models.fields.IntegerField')()),
            ('IDE', self.gf('django.db.models.fields.IntegerField')()),
            ('COM', self.gf('django.db.models.fields.IntegerField')()),
            ('USB2', self.gf('django.db.models.fields.IntegerField')()),
            ('USB3', self.gf('django.db.models.fields.IntegerField')()),
            ('PCI_E_number', self.gf('django.db.models.fields.IntegerField')()),
            ('PCI_E_type', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('graphics', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('form_factor', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('HDMI', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('SLI', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('CrossFire', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('eSATA', self.gf('django.db.models.fields.IntegerField')()),
            ('SATA_RAID', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('Ethernet', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('Ethernet_number', self.gf('django.db.models.fields.IntegerField')()),
            ('WiFi', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('Bluetooth', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('Audio', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('FireWire', self.gf('django.db.models.fields.IntegerField')()),
            ('LPT', self.gf('django.db.models.fields.IntegerField')()),
            ('PS_2', self.gf('django.db.models.fields.IntegerField')()),
            ('DisplayPort', self.gf('django.db.models.fields.IntegerField')()),
            ('SupportedROM', self.gf('django.db.models.fields.TextField')()),
            ('SupportedCPU', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('assets', ['Motherboard'])

        # Adding model 'CPU'
        db.create_table('assets_cpu', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('model_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('firm', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('socket', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('frequency', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('core', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('L1', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('L2', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('L3', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('technology', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('core_number', self.gf('django.db.models.fields.IntegerField')()),
            ('VT', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('integrated_graphics', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('TPD', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('assets', ['CPU'])

        # Adding model 'Case'
        db.create_table('assets_case', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('model_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('firm', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('form_factor', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('supported_mb_types', self.gf('django.db.models.fields.TextField')()),
            ('place_of_power_suply', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('usb_fp', self.gf('django.db.models.fields.IntegerField')()),
            ('audio_fp', self.gf('django.db.models.fields.IntegerField')()),
            ('eSATA_fp', self.gf('django.db.models.fields.IntegerField')()),
            ('eSATA_rp', self.gf('django.db.models.fields.IntegerField')()),
            ('FireWire_fp', self.gf('django.db.models.fields.IntegerField')()),
            ('FireWire_rp', self.gf('django.db.models.fields.IntegerField')()),
            ('number_of_35', self.gf('django.db.models.fields.IntegerField')()),
            ('number_of_525', self.gf('django.db.models.fields.IntegerField')()),
            ('water_ready', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('number_of_extension_slot', self.gf('django.db.models.fields.IntegerField')()),
            ('number_of_fan_places', self.gf('django.db.models.fields.IntegerField')()),
            ('size', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('assets', ['Case'])


    def backwards(self, orm):
        # Deleting model 'Asset'
        db.delete_table('assets_asset')

        # Deleting model 'Payment'
        db.delete_table('assets_payment')

        # Deleting model 'Cash'
        db.delete_table('assets_cash')

        # Deleting model 'Cashless'
        db.delete_table('assets_cashless')

        # Deleting model 'Claim'
        db.delete_table('assets_claim')

        # Deleting model 'Contractor'
        db.delete_table('assets_contractor')

        # Deleting model 'Garanty'
        db.delete_table('assets_garanty')

        # Deleting model 'Asset_type'
        db.delete_table('assets_asset_type')

        # Deleting model 'Status'
        db.delete_table('assets_status')

        # Deleting model 'Budget'
        db.delete_table('assets_budget')

        # Deleting model 'Repair'
        db.delete_table('assets_repair')

        # Deleting model 'Place_Asset'
        db.delete_table('assets_place_asset')

        # Deleting model 'Place'
        db.delete_table('assets_place')

        # Deleting model 'Cartridge'
        db.delete_table('assets_cartridge')

        # Deleting model 'Cartridge_Model_General_Model'
        db.delete_table('assets_cartridge_model_general_model')

        # Deleting model 'Cartridge_General_Model_Printer_Model'
        db.delete_table('assets_cartridge_general_model_printer_model')

        # Deleting model 'Cartridge_Printer'
        db.delete_table('assets_cartridge_printer')

        # Deleting model 'ROM'
        db.delete_table('assets_rom')

        # Deleting model 'Cooler'
        db.delete_table('assets_cooler')

        # Deleting model 'Storage'
        db.delete_table('assets_storage')

        # Deleting model 'Acoustics'
        db.delete_table('assets_acoustics')

        # Deleting model 'Telephone'
        db.delete_table('assets_telephone')

        # Deleting model 'Battery'
        db.delete_table('assets_battery')

        # Deleting model 'Optical_Drive'
        db.delete_table('assets_optical_drive')

        # Deleting model 'Network_equipment'
        db.delete_table('assets_network_equipment')

        # Deleting model 'Printer'
        db.delete_table('assets_printer')

        # Deleting model 'Power_suply'
        db.delete_table('assets_power_suply')

        # Deleting model 'Motherboard'
        db.delete_table('assets_motherboard')

        # Deleting model 'CPU'
        db.delete_table('assets_cpu')

        # Deleting model 'Case'
        db.delete_table('assets_case')


    models = {
        'assets.acoustics': {
            'Meta': {'object_name': 'Acoustics'},
            'acoustics_type': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'firm': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'frequency_interval': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'headphone_jack': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'power_form_usb': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'power_from_battary': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'power_from_circuit': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'remote_control': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'rms': ('django.db.models.fields.IntegerField', [], {}),
            'signal_noise_ratio': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'assets.asset': {
            'Meta': {'object_name': 'Asset'},
            'asset_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['assets.Asset_type']"}),
            'claim': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['assets.Claim']"}),
            'current_place': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'for_asset'", 'to': "orm['assets.Place_Asset']"}),
            'date_of_write_off': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'garanty': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['assets.Garanty']"}),
            'guarantee_period': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'note': ('django.db.models.fields.TextField', [], {}),
            'payment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['assets.Payment']"}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['assets.Status']"})
        },
        'assets.asset_type': {
            'Meta': {'object_name': 'Asset_type'},
            'asset_type': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'catalogue_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'assets.battery': {
            'Meta': {'object_name': 'Battery'},
            'battery_type': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'firm': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'rechargeable': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'assets.budget': {
            'Meta': {'object_name': 'Budget'},
            'end': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start': ('django.db.models.fields.DateTimeField', [], {})
        },
        'assets.cartridge': {
            'Meta': {'object_name': 'Cartridge'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'payment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['assets.Payment']"}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['assets.Status']"})
        },
        'assets.cartridge_general_model_printer_model': {
            'Meta': {'object_name': 'Cartridge_General_Model_Printer_Model'},
            'general_model': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'printer_model': ('django.db.models.fields.CharField', [], {'max_length': '140'})
        },
        'assets.cartridge_model_general_model': {
            'Meta': {'object_name': 'Cartridge_Model_General_Model'},
            'general_model': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '140'})
        },
        'assets.cartridge_printer': {
            'Meta': {'object_name': 'Cartridge_Printer'},
            'cartridge': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['assets.Cartridge']"}),
            'drawdown_date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'installation_date': ('django.db.models.fields.DateTimeField', [], {}),
            'printer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['assets.Asset']"})
        },
        'assets.case': {
            'FireWire_fp': ('django.db.models.fields.IntegerField', [], {}),
            'FireWire_rp': ('django.db.models.fields.IntegerField', [], {}),
            'Meta': {'object_name': 'Case'},
            'audio_fp': ('django.db.models.fields.IntegerField', [], {}),
            'eSATA_fp': ('django.db.models.fields.IntegerField', [], {}),
            'eSATA_rp': ('django.db.models.fields.IntegerField', [], {}),
            'firm': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'form_factor': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'number_of_35': ('django.db.models.fields.IntegerField', [], {}),
            'number_of_525': ('django.db.models.fields.IntegerField', [], {}),
            'number_of_extension_slot': ('django.db.models.fields.IntegerField', [], {}),
            'number_of_fan_places': ('django.db.models.fields.IntegerField', [], {}),
            'place_of_power_suply': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'size': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'supported_mb_types': ('django.db.models.fields.TextField', [], {}),
            'usb_fp': ('django.db.models.fields.IntegerField', [], {}),
            'water_ready': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'assets.cash': {
            'Meta': {'object_name': 'Cash'},
            'contractor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['assets.Contractor']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'})
        },
        'assets.cashless': {
            'Meta': {'object_name': 'Cashless'},
            'contractor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['assets.Contractor']"}),
            'date_of_assets': ('django.db.models.fields.DateTimeField', [], {}),
            'date_of_documents': ('django.db.models.fields.DateTimeField', [], {}),
            'date_of_invoice': ('django.db.models.fields.DateTimeField', [], {}),
            'dates': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'stages': ('django.db.models.fields.TextField', [], {})
        },
        'assets.claim': {
            'Meta': {'object_name': 'Claim'},
            'contractor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['assets.Contractor']"}),
            'date_of_assets': ('django.db.models.fields.DateTimeField', [], {}),
            'date_of_documents': ('django.db.models.fields.DateTimeField', [], {}),
            'date_of_invoice': ('django.db.models.fields.DateTimeField', [], {}),
            'dates': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'stages': ('django.db.models.fields.TextField', [], {})
        },
        'assets.contractor': {
            'Meta': {'object_name': 'Contractor'},
            'contact_name': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'tel': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'tel_of_support': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'})
        },
        'assets.cooler': {
            'Meta': {'object_name': 'Cooler'},
            'cfm': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'destination': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'diametr_of_fans': ('django.db.models.fields.IntegerField', [], {}),
            'firm': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'noise': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'number_of_fans': ('django.db.models.fields.IntegerField', [], {}),
            'rpm': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'sockets': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'type_of_connector': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'assets.cpu': {
            'L1': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'L2': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'L3': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'Meta': {'object_name': 'CPU'},
            'TPD': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'VT': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'core': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'core_number': ('django.db.models.fields.IntegerField', [], {}),
            'firm': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'frequency': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'integrated_graphics': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'model_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'socket': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'technology': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'assets.garanty': {
            'Meta': {'object_name': 'Garanty'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {})
        },
        'assets.motherboard': {
            'Audio': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'Bluetooth': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'COM': ('django.db.models.fields.IntegerField', [], {}),
            'CrossFire': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'DisplayPort': ('django.db.models.fields.IntegerField', [], {}),
            'EFI': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'Ethernet': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'Ethernet_number': ('django.db.models.fields.IntegerField', [], {}),
            'FDD': ('django.db.models.fields.IntegerField', [], {}),
            'FSB': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'FireWire': ('django.db.models.fields.IntegerField', [], {}),
            'HDMI': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'IDE': ('django.db.models.fields.IntegerField', [], {}),
            'LPT': ('django.db.models.fields.IntegerField', [], {}),
            'Meta': {'object_name': 'Motherboard'},
            'PCI_E_number': ('django.db.models.fields.IntegerField', [], {}),
            'PCI_E_type': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'PS_2': ('django.db.models.fields.IntegerField', [], {}),
            'SATA_RAID': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'SLI': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'SupportedCPU': ('django.db.models.fields.TextField', [], {}),
            'SupportedROM': ('django.db.models.fields.TextField', [], {}),
            'USB2': ('django.db.models.fields.IntegerField', [], {}),
            'USB3': ('django.db.models.fields.IntegerField', [], {}),
            'WiFi': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'chipset': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'eSATA': ('django.db.models.fields.IntegerField', [], {}),
            'firm': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'form_factor': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'graphics': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'rom_frequency': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'rom_max_value': ('django.db.models.fields.IntegerField', [], {}),
            'rom_number': ('django.db.models.fields.IntegerField', [], {}),
            'rom_type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'socket': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'assets.network_equipment': {
            'Meta': {'object_name': 'Network_equipment'},
            'SNMP': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'Serial': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'Telnet': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'Web': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'WiFi': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'dhcp_server': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'equipment_type': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'firewall': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'firm': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ipv6_ready': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'model_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'nat': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'rackable': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'vpn': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'assets.optical_drive': {
            'Meta': {'object_name': 'Optical_Drive'},
            'firm': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interface': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'model_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'optical_drive_type': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'assets.payment': {
            'Meta': {'object_name': 'Payment'},
            'cash': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['assets.Cash']"}),
            'cashless': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['assets.Cashless']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'assets.place': {
            'Meta': {'object_name': 'Place'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'place': ('django.db.models.fields.CharField', [], {'max_length': '140'})
        },
        'assets.place_asset': {
            'Meta': {'object_name': 'Place_Asset'},
            'asset': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['assets.Asset']"}),
            'drawdown_date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'installation_date': ('django.db.models.fields.DateTimeField', [], {}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['assets.Place']"}),
            'reason_of_drawdown': ('django.db.models.fields.TextField', [], {})
        },
        'assets.power_suply': {
            'ATX_version': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'Meta': {'object_name': 'Power_suply'},
            'firm': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'modular': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'number_of_molex': ('django.db.models.fields.DecimalField', [], {'max_digits': '1', 'decimal_places': '0'}),
            'number_of_sata': ('django.db.models.fields.DecimalField', [], {'max_digits': '1', 'decimal_places': '0'}),
            'performance': ('django.db.models.fields.DecimalField', [], {'max_digits': '4', 'decimal_places': '2'}),
            'power': ('django.db.models.fields.IntegerField', [], {})
        },
        'assets.printer': {
            'Meta': {'object_name': 'Printer'},
            'color': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'firm': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'network': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'v_print': ('django.db.models.fields.IntegerField', [], {})
        },
        'assets.repair': {
            'Meta': {'object_name': 'Repair'},
            'asset': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['assets.Asset']"}),
            'date_of_failure': ('django.db.models.fields.DateTimeField', [], {}),
            'date_of_write_off': ('django.db.models.fields.DateTimeField', [], {}),
            'date_repair_end': ('django.db.models.fields.DateTimeField', [], {}),
            'date_repair_start': ('django.db.models.fields.DateTimeField', [], {}),
            'failure': ('django.db.models.fields.TextField', [], {}),
            'garanty': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['assets.Garanty']"}),
            'guarantee_period': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'payment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['assets.Payment']"}),
            'repair': ('django.db.models.fields.TextField', [], {})
        },
        'assets.rom': {
            'Meta': {'object_name': 'ROM'},
            'clock_ferquency': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'firm': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'form_factor': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'low_profile': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'model_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'radiator': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'rom_type': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'throughput': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'v': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'assets.status': {
            'Meta': {'object_name': 'Status'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'assets.storage': {
            'Meta': {'object_name': 'Storage'},
            'firm': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'form_factor': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interfaces': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'model_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'rpm': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'v_read': ('django.db.models.fields.IntegerField', [], {}),
            'v_write': ('django.db.models.fields.IntegerField', [], {}),
            'volume': ('django.db.models.fields.IntegerField', [], {})
        },
        'assets.telephone': {
            'DECT': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'GAP': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'Meta': {'object_name': 'Telephone'},
            'alarm_clock': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'aon': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'clock': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'display': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'firm': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'frequency': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'headset': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'speakerphone': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tel_book': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['assets']