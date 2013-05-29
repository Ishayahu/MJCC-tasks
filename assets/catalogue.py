# -*- coding:utf-8 -*-
# coding=<utf8>


# Оперативная память
ROM_form_factors = ['SIMM', 'DIMM', 'FB-DIMM', 'SODIMM', 'MicroDIMM', 'RIMM']
ROM_type=['DDR','DDR2','DDR3','RDRAM','SDRAM']
ROM_firms = ['Corsair', 'Crucial', 'Foxline', 'G.SKILL', 'HP', 'Hynix', 'Kingmax', 'Kingston', 'Patriot Memory', 'Samsung', 'Silicon Power', 'Transcend', 'Acer', 'ADATA', 'AMD', 'Apacer', 'Apple', 'Ceon', 'Chaintech', 'Cisco', 'DELL', 'Digma', 'Elixir', 'EUDAR', 'Exceleram', 'Fujitsu', 'Fujitsu-Siemens', 'Geil', 'GoodRAM', 'Lenovo', 'Micron', 'Mushkin', 'Nanya', 'NCP', 'OCZ', 'PQI', 'Qumo', 'Sony', 'Spectek', 'Sun Microsystems', 'Super Talent', 'TakeMS', 'Team Group', 'Toshiba', 'TwinMOS']
ROM_V = ['128','512','1024','2048','4096','8192']
ROM_clock_frequency = ['100 MHz', '1000 MHz', '1066 MHz', '1100 MHz', '1200 MHz', '133 MHz', '1333 MHz', '1375 MHz', '1600 MHz', '1750 MHz', '1800 MHz', '1866 MHz', '200 MHz', '2000 MHz', '2133 MHz', '2200 MHz', '2250 MHz', '2300 MHz', '2400 MHz', '2600 MHz', '266 MHz', '2666 MHz', '2800 MHz', '333 MHz', '400 MHz', '500 MHz', '533 MHz', '66 MHz', '667 MHz', '750 MHz', '800 MHz']
ROM_throughput = ['10600 Мб/с', '10660 Мб/с', '10666 Мб/с', '10700 Мб/с', '12800 Мб/с', '14000 Мб/с', '14400 Мб/с', '14900 Мб/с', '15000 Мб/с', '1600 Мб/с', '16000 Мб/с', '17000 Мб/с', '17066 Мб/с', '17600 Мб/с', '18000 Мб/с', '18400 Мб/с', '19200 Мб/с', '20800 Мб/с', '2100 Мб/с', '21300 Мб/с', '21330 Мб/с', '22400 Мб/с', '2700 Мб/с', '3200 Мб/с', '4000 Мб/с', '4200 Мб/с', '4300 Мб/с', '5300 Мб/с', '6000 Мб/с', '6400 Мб/с', '8000 Мб/с', '8500 Мб/с', '8800 Мб/с', '9600 Мб/с']
# Кулеры
Cooler_firms = ['Arctic Cooling', 'Cooler Master', 'Corsair', 'Deepcool', 'GlacialTech', 'Ice Hammer', 'Noctua', 'Scythe', 'Thermalright', 'Thermaltake', 'Titan', 'Zalman', '', '@Lux', 'AeroCool', 'AIC', 'Akasa', 'Alpenfoehn', 'Antec', 'ASUS', 'Auras', 'AVC', 'be quiet!', 'BitFenix', 'Chieftec', 'Coolcox', 'Cooler Tech', 'CoolerBoss', 'CROWN', 'DELL', 'DELTA', 'Dynatron', 'Ebmpapst', 'Enermax', 'Espada', 'Evercool', 'Exegate', 'Floston', 'Foxconn', 'G.SKILL', 'GELID Solutions', 'Gembird', 'GRAND', 'Gresso', 'Intel', 'Jetart', 'Kinghun', 'Koolance', 'larkooler', 'LEPA', 'LogicPower', 'Manhattan', 'Maxtron', 'NANOXIA', 'Nexus', 'NOISEBLOCKER', 'NZXT', 'OCZ', 'Pangu', 'PCcooler', 'Phanteks', 'Prolimatech', 'Revoltec', 'SilenX', 'SilverStone', 'Speeze', 'Spire', 'Spiriter', 'STM', 'SUNON', 'Supermicro', 'Sven', 'ThermalFly', 'Vantec', 'Vizo', 'Xigmatek', 'Xilence', 'YATE LOON', 'ZAWARD', 'ZEROtherm']
Cooler_destination = ['для видеокарты', 'для винчестера', 'для корпуса', 'для памяти', 'для процессора', 'для чипсета']
Cooler_sockets = ['Socket A(462)/370', 'Socket AM2', 'Socket AM2+', 'Socket AM3/AM3+/FM1', 'Socket FM2', 'Socket F/С32', 'Socket F+', 'Socket G34', 'Socket 754', 'Socket 939', 'Socket 940', 'Socket 478', 'Socket 775', 'Socket 1155/1156', 'Socket 1366', 'Socket 1567', 'Socket 2011', 'Socket 603', 'Socket 604', 'Socket 771']
Cooler_connector = ['3-pin', '4-pin Molex', '4-pin PWM']
# Хранилища данных
Storage_firms = ['ADATA', 'Hitachi', 'Intel', 'Kingston', 'OCZ', 'Plextor', 'Seagate', 'Silicon Power', 'Synology', 'Toshiba', 'Transcend', 'Western Digital']
Storage_form_factor = ['1.8"', '2.5"', '3.5"']
Storage_interfaces = ['SATA', 'IDE', 'USB', 'FireWire', 'PCI-E', 'SCSI', 'SAS', 'eSATA', 'FireWir e800', 'Fibre Channel', 'Thunderbolt', 'HSDL', 'mSata', 'Ethernet', 'ExpressCard/34', 'ZIF 40 pin', 'mini PCI-E']
Storage_rpm = ['3600 rpm', '4200 rpm', '5200 rpm', '5400 rpm', '5700 rpm', '5900 rpm', '7200 rpm', '10000 rpm', '10025 rpm', '10075 rpm', '10500 rpm', '15000 rpm']
# Колонки и т.п.
Acoustics_firms = ['Creative', 'Defender', 'Dialog', 'Edifier', 'Genius', 'Harman/Kardon', 'JBL', 'JetBalance', 'Logitech', 'Microlab', 'Sven', 'TopDevice', '', '4U', 'A4Tech', 'ACME', 'Acoustic Energy', 'AirTone', 'Altec Lansing', 'Arctic', 'ASUS', 'AVE', 'BBK', 'Bliss', 'Bose', 'Bowers & Wilkins', 'Canyon', 'CBR', 'Cirkuit Planet', 'Codegen SuperPower', 'Comep', 'Cooler Master', 'Corsair', 'CROWN', 'DELL', 'Delux', 'DeTech', 'DIGITUS', 'Divoom', 'DTS', 'Easy Touch', 'ENDEVER', 'Enzatec', 'Espada', 'F&D', 'Fujitsu', 'Fujitsu-Siemens', 'Gear Head', 'Gembird', 'Gemix', 'GIGABYTE', 'GoldenField', 'GRAND', 'Grundig', 'HAMA', 'Hardity', 'Hercules', 'HP', 'iLuv', 'Jet.A', 'k-3', 'Kinghun', 'Klipsch', 'KME', 'Konoos', 'Kreolz', 'KWorld', 'Labtec', 'LOGICFOX', 'Manhattan', 'MB Sound', 'Media-Tech', 'Mobiledata', 'Modecom', 'MSI', 'NAKATOMI', 'NeoDrive', 'ORIENT', 'Ozaki', 'Perfeo', 'Philips', 'Prestigio', 'Ritmix', 'Samsung', 'Sanyoo', 'Scythe', 'SmartTrack', 'SonicGear', 'Sony', 'Sound Pro', 'Soundtronix', 'SPEED', 'SPEEDLINK', 'Sweex', 'T&D', "T'nB", 'Targa', 'Titan', 'Trust', 'UNITY', 'Velton', 'Vicsone', 'VIGOOLE', 'X5Tech', 'XtremeMac', 'Yubz', 'Zalman']
Acoustics_type = ['1.0', '2.0', '2.1', '4.1', '5.0', '5.1', '6.1']
# Телефоны
Telephone_firms = [u'Senao', u'\u0414\u0438\u0430\u043b\u043e\u0433', u'SUPRA', u'Voxtel', u'SwissVoice', u'\u041f\u0430\u043b\u0438\u0445\u0430', u'General Electric', u'Horizont', u'\u041a\u041e\u041c\u041c\u0422\u0415\u041b', u'LG', u'Goodwin', u'Akai', u'Bang & Olufsen', u'ALCOM', u'Plantronics', u'Siemens', u'\u041c\u042d\u041b\u0422', u'Komtel', u'Ritmix', u'Philips', u'Motorola', u'BBK', u'Alcatel', u'Intego', u'\u0412\u0435\u043a\u0442\u043e\u0440', u'Rolsen', u'Gigaset', u'Sagem', u'Euroline', u'\u0422\u0435\u043b\u0444\u043e\u043d', u'\u0424\u0430\u044d\u0442\u043e\u043d', u'\u041a\u043e\u043b\u0438\u0431\u0440\u0438', u'teleGEO', u'\u0422\u0435\u043b\u043b\u0443\u0440', u'LG-Ericsson', u'Switel', u'LG-Nortel', u'Binatone', u'Soul Electronics', u'TeXet', u'Premier', u'Unitel City', u'Orion', u'Rotex', u'\u0422\u0435\u043b\u0442\u0430', u'Shivaki', u'Panasonic']
Telephone_frequency = ['1880-1900 MHz', '240-390 MHz', '307-343 MHz', '31-40 MHz', '900/2400 MHz']
# Батарейки и аккумуляторы
Battery_firms = ['Energizer','Duracell']
Battery_type = ['AA', 'AAA', 'C', 'D', 'PP3 (Krona)']

Optical_Drive_firms = ['3Q', 'Apple', 'ASUS', 'HP', 'Lenovo', 'LG', 'LITE-ON', 'Pioneer', 'Plextor', 'Sony NEC Optiarc', 'Toshiba Samsung Storage Technology', 'Transcend', 'Acer', 'Buffalo', 'Canyon', 'DELL', 'Foxconn', 'Fujitsu', 'Intel', 'Iomega', 'Kreolz', 'Lacie', 'NU', 'ONEXT', 'Panasonic', 'Rovermate', 'Sun Microsystems', 'Supermicro', 'TEAC']
Optical_Drive_type = ['BD-RE', 'BD-ROM', 'BD-ROM/DVD RW', 'BD-ROM/HD DVD-ROM/DVD RW', 'CD-ROM', 'CD-RW', 'DVD RW', 'DVD RW DL', 'DVD-ROM', 'DVD/CD-RW']
Optical_Drive_interfaces = ['eSATA/USB', 'Ethernet/USB', 'FireWire', 'IDE', 'SATA', 'USB']

Network_equipment_firms = [u'Ubiquiti', u'', u'Nano', u'SIVVA', u'3COM', u'Huawei', u'Winstars', u'CCK', u'HAMA', u'Compex', u'Linkpro', u'Galaxy Innovations', u'Allied Telesyn', u'S-iTECH', u'Level One', u'Skylink', u'Buro', u'SPEEDLINK', u'GIGABYTE', u'DIGITUS', u'Rovermate', u'GetNet', u'Normann', u'Porto', u'EUSSO', u'LOGICFOX', u'Mobiledata', u'Cisco', u'2N', u'Z-Com', u'Pentagram', u'Carelink', u'Globo', u'Edimax', u'TRENDnet', u'Alwise', u'Sweex', u'CYBER', u'QTECH', u'Upvel', u'Fortinet', u'Qbiq', u'Novatel Wireless', u'eXtreme', u'Petatel', u'\u041c\u0422\u0421', u'HP', u'Proxim', u'Espada', u'DrayTek', u'Eye-Fi', u'Cyclone', u'Emtec', u'Option', u'STLab', u'Yota', u'AMX', u'X-Micro', u'Sony', u'Throw', u'EnGenius', u'Motorola', u'Linksys', u'Samsung', u'D-link', u'U.S.Robotics', u'Asotel', u'Qumo', u'Deppa', u'NCENTRA', u'Loopcomm', u'Western Digital', u'Buffalo', u'ORIENT', u'Planet', u'MOXA', u'Seowon Intech', u'SIYOTEAM', u'Nortel', u'CBR', u'Terminal Equipment', u'LogicPower', u'ASUS', u'BandRich', u'Opticum', u'\u0422\u041e\u041d\u041a', u'Novacom Wireless', u'Senao', u'EDUP', u'Vertex', u'Multico', u'Alfa Network', u'Creative', u'Genius', u'NeoDrive', u'C-net', u'SMC', u'X-NET', u'Intellinet', u'Gemix', u'Arctic', u'OXO Electronics', u'Popcorn Hour', u'3Q', u'Symanitron', u'BBK', u'Intel', u'ZTE', u'Palmexx', u'Powchip', u'Grand-X', u'Sparklan', u'Euroline', u'TP-LINK', u'Media-Tech', u'Edge-Core', u'x3', u'MicroNet', u'Welltech', u'DT-Link', u'Belkin', u'Surecom', u'Canyon', u'NETGEAR', u'Panasonic', u'Mobidick', u'Tenda', u'MSI', u'Dynamode', u'LEXAND', u'Pheenet', u'Brickcom', u'CLiPtec', u'AirTies', u'ZyXEL', u'SerteC', u'LG', u'Juniper', u'Acorp', u'Crestron', u'Kreolz', u'AirLive', u'eVidence', u'REPOTEC', u'Promate', u'Sandisk', u'Philips', u'InterStep', u'Egreat', u'Alcatel', u'BEWARD', u'DELL', u'AudioCodes', u'Netis', u'Encore', u'Sitecom', u'ARC Wireless', u'Apple', u'Gemtek', u'EWEL', u'Gembird', u'Dynamix', u'MikroTik', u'Trust']
Network_equipment_type = ['Router','Switch','AP','Repeater','Smart Switch']
Network_equipment_WiFi_type = ['802.11a', '802.11a/b/g', '802.11ac', '802.11b', '802.11g', '802.11n']

Printer_firm = ['Brother', 'Canon', 'Epson', 'HP', 'Kyocera', 'Lexmark', 'OKI', 'Panasonic', 'Ricoh', 'Samsung', 'Toshiba', 'Xerox', 'DELL', 'Develop', 'Flora', 'Fujifilm', 'Gestetner', 'HiTi', 'KIP', 'Konica Minolta', 'Lomond', 'MB', 'Mimaki', 'Mitsubishi Electric', 'Mutoh', 'Oce', 'Pantum', 'Philips', 'Polaroid', 'Riso', 'Roland', 'ROWE', 'Seiko', 'Sharp', 'Shinco', 'Sony']

Power_suply_firm = ['AeroCool', 'Chieftec', 'Cooler Master', 'Corsair', 'FSP Group', 'HIPER', 'HIPRO', 'IN WIN', 'LinkWorld', 'OCZ', 'Sea Sonic Electronics', 'Thermaltake', '', '5bites', '@Lux', 'Antec', 'Aopen', 'Ascot', 'AXES Line', 'be quiet!', 'Codegen SuperPower', 'COUGAR', 'CROWN', 'CWT', 'DELTA ELECTRONICS', 'DeTech', 'DTS', 'EMACS', 'Enermax', 'Enhance Electronics', 'Espada', 'ETG', 'Exegate', 'FinePower', 'Floston', 'FOX', 'Foxline', 'Fractal Design', 'Gembird', 'GIGABYTE', 'GoldenField', 'Gresso', 'HEC', 'HIGH POWER', 'HuntKey', 'Ice Hammer', 'Invenom', 'LEPA', 'LogicPower', 'NaviPower', 'Nexus', 'NZXT', 'Pangu', 'PC Power & Cooling', 'PowerBox', 'PowerColor', 'PowerExpert', 'ProLogiX', 'RaidMAX', 'Scythe', 'SilverStone', 'Spire', 'STM', 'Velton', 'Winard', 'XFX', 'Xigmatek', 'Xilence', 'Zalman']
Power_ATX_version = ['1.3', '2.0', '2.01', '2.03', '2.1', '2.2', '2.3']

Motherboard_firm = ['ASRock', 'ASUS', 'Biostar', 'ECS', 'Foxconn', 'GIGABYTE', 'Intel', 'MSI', 'Pegatron', 'Sapphire', 'Supermicro', 'ZOTAC', '3Q', 'ABIT', 'EPoX', 'EVGA', 'Fujitsu', 'ITZR', 'Jetway', 'PCCHIPS', 'Tyan', 'VIA', 'Wibtek']
Motherboard_chipset = ['AMD 480X CrossFire', 'AMD 690G', 'AMD 740G', 'AMD 760 MPX', 'AMD 760G', 'AMD 770', 'AMD 780V', 'AMD 785G', 'AMD 790FX', 'AMD 790GX', 'AMD 790X', 'AMD 8111', 'AMD 8131', 'AMD 8151', 'AMD 870', 'AMD 880G', 'AMD 890FX', 'AMD 890GX', 'AMD 970', 'AMD 990FX', 'AMD 990X', 'AMD A45', 'AMD A50M', 'AMD A55', 'AMD A55E', 'AMD A68', 'AMD A75', 'AMD A85', 'AMD A85X', 'AMD Hudson E1', 'AMD Hudson-D1', 'AMD Hudson-D3', 'AMD M690E', 'AMD RS785', 'AMD RX881', 'AMD SR5650', 'AMD SR5670', 'AMD SR5690', 'Broadcom HT1000', 'Intel 3000', 'Intel 3200', 'Intel 3210', 'Intel 3400', 'Intel 3420', 'Intel 3450', 'Intel 5000P', 'Intel 5000V', 'Intel 5000X', 'Intel 5100', 'Intel 5400', 'Intel 5500', 'Intel 5520', 'Intel 845', 'Intel 845GV', 'Intel 848P', 'Intel 865G', 'Intel 865GV', 'Intel 915P', 'Intel 945GC', 'Intel 945GM', 'Intel 945GSE', 'Intel 955X', 'Intel B75', 'Intel C202', 'Intel C204', 'Intel C206', 'Intel C216', 'Intel C600', 'Intel C602', 'Intel C602-A', 'Intel C602J', 'Intel C604', 'Intel C606', 'Intel E7210', 'Intel E7221', 'Intel E7230', 'Intel E7320', 'Intel E7500', 'Intel E7501', 'Intel E7505', 'Intel E7520', 'Intel E7525', 'Intel G31', 'Intel G41', 'Intel G43', 'Intel G45', 'Intel G965', 'Intel H55', 'Intel H57 Express', 'Intel H61', 'Intel H67', 'Intel H77', 'Intel HM70', 'Intel ICH8M', 'Intel ICH9', 'Intel ICH9R', 'Intel NM10', 'Intel NM70', 'Intel P31 Express', 'Intel P43', 'Intel P55', 'Intel P67', 'Intel P67(B3)', 'Intel P965', 'Intel Q43', 'Intel Q45', 'Intel Q57', 'Intel Q67', 'Intel Q77', 'Intel QM67', 'Intel QM77', 'Intel S1260', 'Intel X38', 'Intel X48', 'Intel X58', 'Intel X79', 'Intel Z68', 'Intel Z75', 'Intel Z77', 'Intel Z87', 'NVIDIA GeForce 6100', 'NVIDIA GeForce 6150 SE', 'NVIDIA GeForce 7025', 'NVIDIA MCP55 Pro', 'NVIDIA MCP61', 'NVIDIA MCP61P', 'NVIDIA MCP68S', 'NVIDIA MCP79', 'NVIDIA MCP7A-ION', 'NVIDIA nForce 520 LE', 'NVIDIA nForce 550', 'NVIDIA nForce 570 Ultra', 'NVIDIA nForce 630a', 'NVIDIA nForce 680i SLI', 'NVIDIA nForce 720D', 'NVIDIA nForce 750a SLI', 'NVIDIA nForce 980a SLI', 'NVIDIA nForce Professional 2200', 'NVIDIA nForce Professional 3600', 'NVIDIA nForce2', 'NVIDIA nForce3 250', 'NVIDIA nForce4', 'NVIDIA nForce4 SLI X16', 'NVIDIA nForce4 Ultra', 'NVIDIA NFP3600', 'ServerWorks BCM5785', 'ServerWorks Grand Champion LE', 'ServerWorks HT1000', 'SiS 661GX', 'SiS 662', 'SiS 741GX', 'ULi M1689', 'VIA CLE266', 'VIA CN700', 'VIA CN896', 'VIA K8M800', 'VIA K8T800', 'VIA K8T800 Pro', 'VIA P4M800', 'VIA P4M890', 'VIA P4M900', 'VIA VX800', 'VIA VX900', 'VIA VX900H']
Motherboard_rom_types = ['DDR DIMM', 'DDR2 DIMM', 'DDR2 FB-DIMM', 'DDR2 SO-DIMM', 'DDR2/DDR3 DIMM', 'DDR3 DIMM', 'DDR3 RDIMM/UDIMM', 'DDR3 SO-DIMM']
Motherboard_pci_e_types = ['1.0','2.0','3.0']
Motherboard_integrated_graphics = ['','AMD Llano', 'AMD Radeon HD 6320', 'AMD Radeon HD 7340', 'AMD Zacate', 'Aspeed AST1300', 'Aspeed AST2050', 'Aspeed AST2150', 'Aspeed AST2300', 'ATI ES1000', 'ATI Radeon HD 4200', 'ATI Radeon HD 4250', 'ATI Radeon HD 4290', 'ATI Radeon HD 6290', 'ATI Radeon HD 6310', 'ATI Radeon HD2100', 'ATI Radeon HD3000', 'ATI Radeon HD3100', 'ATI Radeon HD3300', 'ATI Radeon HD6310', 'ATI Radeon X1250', 'ATI Rage XL', 'ATI Rage XL PCI', 'Intel Extreme Graphics 2', 'Intel GMA 3000', 'Intel GMA 3100', 'Intel GMA 3150', 'Intel GMA 4500', 'Intel GMA 950', 'Intel GMA X4500', 'Intel GMA3600', 'Intel GMA3650', 'Intel MCH', 'Intel PowerVR SGX545', 'Matrox G200', 'Matrox G200e', 'Matrox G200eW', 'NVIDIA GeForce 6100', 'NVIDIA GeForce 6150', 'NVIDIA GeForce 7025', 'NVIDIA GeForce 9400', 'NVIDIA GeForce GT 520', 'SiS Mirage', 'SiS Real256', 'VIA Chrome9', 'VIA UniChrome Pro', 'XGI Volari Z7', 'XGI Volari Z9s', 'XGI XG20']
Motherboard_form_factor = ['ATX', 'DTX', 'EATX', 'Em-ITX', 'FlexATX', 'HPTX', 'mBTX', 'microATX', 'mini-DTX', 'mini-ITX', 'SSI CEB', 'SSI EEB', 'SSI MEB', 'SWTX', 'thin mini-ITX', 'XL-ATX', 'NonStandart']
Motherboard_sata_raid = ['0', '1', '10', '5', 'JBOD', '']
Motherboard_audio = ["AC'97", 'EAX', 'HDA', '']

CPU_firm = ['AMD','Intel']
CPU_core = ['Abu Dhabi', 'Agena', 'Allendale', 'Athens', 'Banias', 'Barcelona', 'Beckton', 'Bloomfield', 'Brisbane', 'Budapest', 'Callisto', 'Cedar Mill', 'Clarkdale', 'Clovertown', 'Conroe', 'Conroe-CL', 'Conroe-L', 'Dempsey', 'Deneb', 'Dothan', 'Dunnington', 'Egypt', 'Gainestown', 'Gallatin', 'Gulftown', 'Harpertown', 'Heka', 'Interlagos', 'Irwindale', 'Istanbul', 'Italy', 'Ivy Bridge', 'Ivy Bridge-H2', 'Kentsfield', 'Lisbon', 'Llano', 'Lynnfield', 'Magny-Cours', 'Merom', 'Nocona', 'Northwood', 'Paxville', 'Penryn', 'Prescott', 'Presler', 'Prestonia', 'Propus', 'Rana', 'Regor', 'Sandy Bridge', 'Sandy Bridge-E', 'Sandy Bridge-EN', 'Sandy Bridge-EP', 'Santa Ana', 'Santa Rosa', 'Sargas', 'Seoul', 'Shanghai', 'Sledgehammer', 'Smithfield', 'Sparta', 'Thuban', 'Tigerton', 'Trinity', 'Troy', 'Tulsa', 'Valencia', 'Vishera', 'Westmere-EX', 'Windsor', 'Wolfdale', 'Woodcrest', 'Yonah', 'Yorkfield', 'Zambezi', 'Zosma']
CPU_L1 = ['8 Kb', '16 Kb', '48 Kb', '64 Kb', '128 Kb']
CPU_L2 = ['128 Kb', '256 Kb', '512 Kb', '1024 Kb', '1536 Kb', '2048 Kb', '2560 Kb', '3072 Kb', '4096 Kb', '6144 Kb', '8192 Kb', '9216 Kb', '12288 Kb', '16384 Kb']
CPU_L3 = ['',]
CPU_technology = ['130 nm', '22 nm', '32 nm', '45 nm', '65 nm', '90 nm']

Case_firm = ['AeroCool', 'Cooler Master', 'Corsair', 'Foxconn', 'GIGABYTE', 'IN WIN', 'JSP-TECH', 'SilverStone', 'Storm', 'Thermaltake', 'Winsis', 'Zalman', '', '3Cott', '3Q', '3R System', '4U', '@Lux', 'AIGO', 'AiO', 'AirTone', 'Akasa', 'Antec', 'Aopen', 'AplusCase', 'Arctic Cooling', 'ARESZE', 'Ascot', 'ASUS', 'Autograph', 'AXES Line', 'AZZA', 'BitFenix', 'Brightwins', 'BTC', 'CASECOM Technology', 'CasePoint', 'CFI Group', 'Chenbro', 'Chieftec', 'Classix', 'Codegen SuperPower', 'COLORSit', 'COODMax', 'COUGAR', 'Coupden', 'Credo', 'CROWN', 'Delux', 'DeTech', 'DTS', 'DVQ', 'Enermax', 'ENlight', 'Espada', 'ETG', 'Eurocase', 'Evolution', 'Exegate', 'Fast', 'Floston', 'FORUM Computers', 'FOX', 'Foxline', 'Fractal Design', 'FrimeCom', 'Frisby', 'Frontier', 'FSP Group', 'FST', 'GameTiger', 'Gembird', 'GMC', 'GoldenField', 'GRAND', 'Gresso', 'Griffon', 'HEDY', 'HKC', 'HQ-Tech', 'HuntKey', 'iBOX', 'iCute', 'IKONIK', 'Impression', 'Intel', 'Inter-Tech', 'Invenom', 'JCP', 'JET', 'JNC', 'KIMPRO', 'Kinghun', 'KM Korea', 'KME', 'Krauler', 'LanCool', 'Lct Technology Inc.', 'Lian Li', 'LinkWorld', 'Logic Concept Technology', 'LogicPower', 'LOOP', 'MaxPoint', 'MEC', 'Microlab', 'Microtech', 'Modecom', 'Moneual', 'Morex', 'NANOXIA', 'NaviPower', 'NTS', 'NZXT', 'Optimum', 'Pangu', 'Point of View', 'PowerCase', 'PowerExpert', 'ProLogiX', 'Prosource', 'RaidMAX', 'Scythe', 'SeulCase', 'Sharkoon', 'Solarbox', 'SOLIX', 'SPEED', 'Spire', 'Star Technology', 'STC', 'Streacom', 'Supermicro', 'Sven', 'TACENS', 'Targa', 'TEXCONN', 'Tracer', 'Trin', 'Tsunami', 'V-King', 'V-Tech', 'Velton', 'ViewApple Group', 'Winard', 'Winstar', 'Xclio', 'Xigmatek', 'Xilence', 'Yeong Yang', 'Yuhanhi Tec', 'Zignum']
Case_power_suply_place = ['top','bottom']
Case_form_factor = ['Full-Desktop', 'Full-Tower', 'Micro-Tower', 'Midi-Tower', 'Mini-Tower', 'Slim-Desktop', 'Super-Tower']




Sockets = ['AM2', 'AM2+', 'AM3', 'AM3+', 'BGA437', 'C32', 'FM1', 'FM2', 'FS1r2', 'G2', 'G2 (rPGA 988B)', 'G34', 'LGA1150', 'LGA1155', 'LGA1156', 'LGA1356', 'LGA1366', 'LGA2011', 'LGA771', 'LGA775', 'M', 'S1207 (Socket F)', 'S462', 'S478', 'S479', 'S603', 'S604', 'S754', 'S939', 'S940']
Ethernet_types = ['10 Mb/s','100 Mb/s','1 Gb/s','10 Gb/s','']
WiFi_types = ['802.11a/b/g', '802.11n','802.11ac','']



# [b.strip() for b in a.strip().split('\n')]