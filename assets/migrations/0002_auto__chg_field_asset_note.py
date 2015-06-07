# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Asset.note'
        db.alter_column('assets_asset', 'note', self.gf('django.db.models.fields.TextField')(null=True))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Asset.note'
        raise RuntimeError("Cannot reverse this migration. 'Asset.note' and its values cannot be restored.")

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
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
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