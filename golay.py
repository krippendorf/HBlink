#!/usr/bin/env python
#
# This work is licensed under the Creative Attribution-NonCommercial-ShareAlike
# 3.0 Unported License.To view a copy of this license, visit
# http://creativecommons.org/licenses/by-nc-sa/3.0/ or send a letter to
# Creative Commons, 444 Castro Street, Suite 900, Mountain View,
# California, 94041, USA.

from __future__ import print_function
from bitarray import bitarray

# Does anybody read this stuff? There's a PEP somewhere that says I should do this.
__author__     = 'Cortney T. Buffington, N0MJS'
__copyright__  = 'Copyright (c) 2016 Cortney T. Buffington, N0MJS and the K0USY Group'
__credits__    = 'Jonathan Naylor, G4KLX who many parts of this were thankfully borrowed from'
__license__    = 'Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported'
__maintainer__ = 'Cort Buffington, N0MJS'
__email__      = 'n0mjs@me.com'


X18     = 0x00040000   # vector representation of X^18
X11     = 0x00000800   # vector representation of X^11
MASK8   = 0xfffff800   # auxiliary vector for testing
GENPOL  = 0x00000c75   # generator polinomial, g(x)

ENCODE_2087 = (
	0x0000, 0xB08E, 0xE093, 0x501D, 0x70A9, 0xC027, 0x903A, 0x20B4, 0x60DC, 0xD052, 0x804F, 0x30C1, 0x1075, 0xA0FB,
    0xF0E6, 0x4068, 0x7036, 0xC0B8, 0x90A5, 0x202B, 0x009F, 0xB011, 0xE00C, 0x5082, 0x10EA, 0xA064, 0xF079, 0x40F7,
    0x6043, 0xD0CD, 0x80D0, 0x305E, 0xD06C, 0x60E2, 0x30FF, 0x8071, 0xA0C5, 0x104B, 0x4056, 0xF0D8, 0xB0B0, 0x003E,
    0x5023, 0xE0AD, 0xC019, 0x7097, 0x208A, 0x9004, 0xA05A, 0x10D4, 0x40C9, 0xF047, 0xD0F3, 0x607D, 0x3060, 0x80EE,
    0xC086, 0x7008, 0x2015, 0x909B, 0xB02F, 0x00A1, 0x50BC, 0xE032, 0x90D9, 0x2057, 0x704A, 0xC0C4, 0xE070, 0x50FE,
    0x00E3, 0xB06D, 0xF005, 0x408B, 0x1096, 0xA018, 0x80AC, 0x3022, 0x603F, 0xD0B1, 0xE0EF, 0x5061, 0x007C, 0xB0F2,
	0x9046, 0x20C8, 0x70D5, 0xC05B, 0x8033, 0x30BD, 0x60A0, 0xD02E, 0xF09A, 0x4014, 0x1009, 0xA087, 0x40B5, 0xF03B,
    0xA026, 0x10A8, 0x301C, 0x8092, 0xD08F, 0x6001, 0x2069, 0x90E7, 0xC0FA, 0x7074, 0x50C0, 0xE04E, 0xB053, 0x00DD,
    0x3083, 0x800D, 0xD010, 0x609E, 0x402A, 0xF0A4, 0xA0B9, 0x1037, 0x505F, 0xE0D1, 0xB0CC, 0x0042, 0x20F6, 0x9078,
    0xC065, 0x70EB, 0xA03D, 0x10B3, 0x40AE, 0xF020, 0xD094, 0x601A, 0x3007, 0x8089, 0xC0E1, 0x706F, 0x2072, 0x90FC,
    0xB048, 0x00C6, 0x50DB, 0xE055, 0xD00B, 0x6085, 0x3098, 0x8016, 0xA0A2, 0x102C, 0x4031, 0xF0BF, 0xB0D7, 0x0059,
    0x5044, 0xE0CA, 0xC07E, 0x70F0, 0x20ED, 0x9063, 0x7051, 0xC0DF, 0x90C2, 0x204C, 0x00F8, 0xB076, 0xE06B, 0x50E5,
	0x108D, 0xA003, 0xF01E, 0x4090, 0x6024, 0xD0AA, 0x80B7, 0x3039, 0x0067, 0xB0E9, 0xE0F4, 0x507A, 0x70CE, 0xC040,
    0x905D, 0x20D3, 0x60BB, 0xD035, 0x8028, 0x30A6, 0x1012, 0xA09C, 0xF081, 0x400F, 0x30E4, 0x806A, 0xD077, 0x60F9,
    0x404D, 0xF0C3, 0xA0DE, 0x1050, 0x5038, 0xE0B6, 0xB0AB, 0x0025, 0x2091, 0x901F, 0xC002, 0x708C, 0x40D2, 0xF05C,
    0xA041, 0x10CF, 0x307B, 0x80F5, 0xD0E8, 0x6066, 0x200E, 0x9080, 0xC09D, 0x7013, 0x50A7, 0xE029, 0xB034, 0x00BA,
    0xE088, 0x5006, 0x001B, 0xB095, 0x9021, 0x20AF, 0x70B2, 0xC03C, 0x8054, 0x30DA, 0x60C7, 0xD049, 0xF0FD, 0x4073,
    0x106E, 0xA0E0, 0x90BE, 0x2030, 0x702D, 0xC0A3, 0xE017, 0x5099, 0x0084, 0xB00A, 0xF062, 0x40EC, 0x10F1, 0xA07F,
	0x80CB, 0x3045, 0x6058, 0xD0D6)

DECODE_1987 = (
	0x00000, 0x00001, 0x00002, 0x00003, 0x00004, 0x00005, 0x00006, 0x00007, 0x00008, 0x00009, 0x0000A, 0x0000B, 0x0000C, 
	0x0000D, 0x0000E, 0x24020, 0x00010, 0x00011, 0x00012, 0x00013, 0x00014, 0x00015, 0x00016, 0x00017, 0x00018, 0x00019, 
	0x0001A, 0x0001B, 0x0001C, 0x0001D, 0x48040, 0x01480, 0x00020, 0x00021, 0x00022, 0x00023, 0x00024, 0x00025, 0x00026, 
	0x24008, 0x00028, 0x00029, 0x0002A, 0x24004, 0x0002C, 0x24002, 0x24001, 0x24000, 0x00030, 0x00031, 0x00032, 0x08180, 
	0x00034, 0x00C40, 0x00036, 0x00C42, 0x00038, 0x43000, 0x0003A, 0x43002, 0x02902, 0x24012, 0x02900, 0x24010, 0x00040, 
	0x00041, 0x00042, 0x00043, 0x00044, 0x00045, 0x00046, 0x00047, 0x00048, 0x00049, 0x0004A, 0x02500, 0x0004C, 0x0004D, 
	0x48010, 0x48011, 0x00050, 0x00051, 0x00052, 0x21200, 0x00054, 0x00C20, 0x48008, 0x48009, 0x00058, 0x00059, 0x48004, 
	0x48005, 0x48002, 0x48003, 0x48000, 0x48001, 0x00060, 0x00061, 0x00062, 0x00063, 0x00064, 0x00C10, 0x10300, 0x0B000, 
	0x00068, 0x00069, 0x01880, 0x01881, 0x40181, 0x40180, 0x24041, 0x24040, 0x00070, 0x00C04, 0x00072, 0x00C06, 0x00C01, 
	0x00C00, 0x00C03, 0x00C02, 0x05204, 0x00C0C, 0x48024, 0x48025, 0x05200, 0x00C08, 0x48020, 0x48021, 0x00080, 0x00081, 
	0x00082, 0x00083, 0x00084, 0x00085, 0x00086, 0x00087, 0x00088, 0x00089, 0x0008A, 0x50200, 0x0008C, 0x0A800, 0x01411, 
	0x01410, 0x00090, 0x00091, 0x00092, 0x08120, 0x00094, 0x00095, 0x04A00, 0x01408, 0x00098, 0x00099, 0x01405, 0x01404, 
	0x01403, 0x01402, 0x01401, 0x01400, 0x000A0, 0x000A1, 0x000A2, 0x08110, 0x000A4, 0x000A5, 0x42400, 0x42401, 0x000A8, 
	0x000A9, 0x01840, 0x01841, 0x40141, 0x40140, 0x24081, 0x24080, 0x000B0, 0x08102, 0x08101, 0x08100, 0x000B4, 0x08106, 
	0x08105, 0x08104, 0x20A01, 0x20A00, 0x08109, 0x08108, 0x01423, 0x01422, 0x01421, 0x01420, 0x000C0, 0x000C1, 0x000C2, 
	0x000C3, 0x000C4, 0x000C5, 0x000C6, 0x000C7, 0x000C8, 0x000C9, 0x01820, 0x01821, 0x20600, 0x40120, 0x16000, 0x16001, 
	0x000D0, 0x000D1, 0x42801, 0x42800, 0x03100, 0x18200, 0x03102, 0x18202, 0x000D8, 0x000D9, 0x48084, 0x01444, 0x48082, 
	0x01442, 0x48080, 0x01440, 0x000E0, 0x32000, 0x01808, 0x04600, 0x40109, 0x40108, 0x0180C, 0x4010A, 0x01802, 0x40104, 
	0x01800, 0x01801, 0x40101, 0x40100, 0x01804, 0x40102, 0x0A408, 0x08142, 0x08141, 0x08140, 0x00C81, 0x00C80, 0x00C83, 
	0x00C82, 0x0A400, 0x0A401, 0x01810, 0x01811, 0x40111, 0x40110, 0x01814, 0x40112, 0x00100, 0x00101, 0x00102, 0x00103, 
	0x00104, 0x00105, 0x00106, 0x41800, 0x00108, 0x00109, 0x0010A, 0x02440, 0x0010C, 0x0010D, 0x0010E, 0x02444, 0x00110, 
	0x00111, 0x00112, 0x080A0, 0x00114, 0x00115, 0x00116, 0x080A4, 0x00118, 0x00119, 0x15000, 0x15001, 0x02822, 0x02823, 
	0x02820, 0x02821, 0x00120, 0x00121, 0x00122, 0x08090, 0x00124, 0x00125, 0x10240, 0x10241, 0x00128, 0x00129, 0x0012A, 
	0x24104, 0x09400, 0x400C0, 0x02810, 0x24100, 0x00130, 0x08082, 0x08081, 0x08080, 0x31001, 0x31000, 0x02808, 0x08084, 
	0x02806, 0x0808A, 0x02804, 0x08088, 0x02802, 0x02803, 0x02800, 0x02801, 0x00140, 0x00141, 0x00142, 0x02408, 0x00144, 
	0x00145, 0x10220, 0x10221, 0x00148, 0x02402, 0x02401, 0x02400, 0x400A1, 0x400A0, 0x02405, 0x02404, 0x00150, 0x00151, 
	0x00152, 0x02418, 0x03080, 0x03081, 0x03082, 0x03083, 0x09801, 0x09800, 0x02411, 0x02410, 0x48102, 0x09804, 0x48100, 
	0x48101, 0x00160, 0x00161, 0x10204, 0x10205, 0x10202, 0x40088, 0x10200, 0x10201, 0x40085, 0x40084, 0x02421, 0x02420, 
	0x40081, 0x40080, 0x10208, 0x40082, 0x41402, 0x080C2, 0x41400, 0x080C0, 0x00D01, 0x00D00, 0x10210, 0x10211, 0x40095, 
	0x40094, 0x02844, 0x080C8, 0x40091, 0x40090, 0x02840, 0x02841, 0x00180, 0x00181, 0x00182, 0x08030, 0x00184, 0x14400, 
	0x22201, 0x22200, 0x00188, 0x00189, 0x0018A, 0x08038, 0x40061, 0x40060, 0x40063, 0x40062, 0x00190, 0x08022, 0x08021, 
	0x08020, 0x03040, 0x03041, 0x08025, 0x08024, 0x40C00, 0x40C01, 0x08029, 0x08028, 0x2C000, 0x2C001, 0x01501, 0x01500, 
	0x001A0, 0x08012, 0x08011, 0x08010, 0x40049, 0x40048, 0x08015, 0x08014, 0x06200, 0x40044, 0x30400, 0x08018, 0x40041, 
	0x40040, 0x40043, 0x40042, 0x08003, 0x08002, 0x08001, 0x08000, 0x08007, 0x08006, 0x08005, 0x08004, 0x0800B, 0x0800A, 
	0x08009, 0x08008, 0x40051, 0x40050, 0x02880, 0x0800C, 0x001C0, 0x001C1, 0x64000, 0x64001, 0x03010, 0x40028, 0x08C00, 
	0x08C01, 0x40025, 0x40024, 0x02481, 0x02480, 0x40021, 0x40020, 0x40023, 0x40022, 0x03004, 0x03005, 0x08061, 0x08060, 
	0x03000, 0x03001, 0x03002, 0x03003, 0x0300C, 0x40034, 0x30805, 0x30804, 0x03008, 0x40030, 0x30801, 0x30800, 0x4000D, 
	0x4000C, 0x08051, 0x08050, 0x40009, 0x40008, 0x10280, 0x4000A, 0x40005, 0x40004, 0x01900, 0x40006, 0x40001, 0x40000, 
	0x40003, 0x40002, 0x14800, 0x08042, 0x08041, 0x08040, 0x03020, 0x40018, 0x08045, 0x08044, 0x40015, 0x40014, 0x08049, 
	0x08048, 0x40011, 0x40010, 0x40013, 0x40012, 0x00200, 0x00201, 0x00202, 0x00203, 0x00204, 0x00205, 0x00206, 0x00207, 
	0x00208, 0x00209, 0x0020A, 0x50080, 0x0020C, 0x0020D, 0x0020E, 0x50084, 0x00210, 0x00211, 0x00212, 0x21040, 0x00214, 
	0x00215, 0x04880, 0x04881, 0x00218, 0x00219, 0x0E001, 0x0E000, 0x0021C, 0x0021D, 0x04888, 0x0E004, 0x00220, 0x00221, 
	0x00222, 0x00223, 0x00224, 0x00225, 0x10140, 0x10141, 0x00228, 0x00229, 0x0022A, 0x24204, 0x12401, 0x12400, 0x24201, 
	0x24200, 0x00230, 0x00231, 0x00232, 0x21060, 0x2A000, 0x2A001, 0x2A002, 0x2A003, 0x20881, 0x20880, 0x20883, 0x20882, 
	0x05040, 0x05041, 0x05042, 0x24210, 0x00240, 0x00241, 0x00242, 0x21010, 0x00244, 0x46000, 0x10120, 0x10121, 0x00248, 
	0x00249, 0x0024A, 0x21018, 0x20480, 0x20481, 0x20482, 0x20483, 0x00250, 0x21002, 0x21001, 0x21000, 0x18081, 0x18080, 
	0x21005, 0x21004, 0x12800, 0x12801, 0x21009, 0x21008, 0x05020, 0x05021, 0x48200, 0x48201, 0x00260, 0x00261, 0x10104, 
	0x04480, 0x10102, 0x10103, 0x10100, 0x10101, 0x62002, 0x62003, 0x62000, 0x62001, 0x05010, 0x05011, 0x10108, 0x10109, 
	0x0500C, 0x21022, 0x21021, 0x21020, 0x05008, 0x00E00, 0x10110, 0x10111, 0x05004, 0x05005, 0x05006, 0x21028, 0x05000, 
	0x05001, 0x05002, 0x05003, 0x00280, 0x00281, 0x00282, 0x50008, 0x00284, 0x00285, 0x04810, 0x22100, 0x00288, 0x50002, 
	0x50001, 0x50000, 0x20440, 0x20441, 0x50005, 0x50004, 0x00290, 0x00291, 0x04804, 0x04805, 0x04802, 0x18040, 0x04800, 
	0x04801, 0x20821, 0x20820, 0x50011, 0x50010, 0x0480A, 0x01602, 0x04808, 0x01600, 0x002A0, 0x002A1, 0x04441, 0x04440, 
	0x002A4, 0x002A5, 0x04830, 0x04444, 0x06100, 0x20810, 0x50021, 0x50020, 0x06104, 0x20814, 0x50025, 0x50024, 0x20809, 
	0x20808, 0x13000, 0x08300, 0x04822, 0x2080C, 0x04820, 0x04821, 0x20801, 0x20800, 0x20803, 0x20802, 0x20805, 0x20804, 
	0x04828, 0x20806, 0x002C0, 0x002C1, 0x04421, 0x04420, 0x20408, 0x18010, 0x2040A, 0x18012, 0x20404, 0x20405, 0x50041, 
	0x50040, 0x20400, 0x20401, 0x20402, 0x20403, 0x18005, 0x18004, 0x21081, 0x21080, 0x18001, 0x18000, 0x04840, 0x18002, 
	0x20414, 0x1800C, 0x21089, 0x21088, 0x20410, 0x18008, 0x20412, 0x1800A, 0x04403, 0x04402, 0x04401, 0x04400, 0x10182, 
	0x04406, 0x10180, 0x04404, 0x01A02, 0x0440A, 0x01A00, 0x04408, 0x20420, 0x40300, 0x20422, 0x40302, 0x04413, 0x04412, 
	0x04411, 0x04410, 0x18021, 0x18020, 0x10190, 0x18022, 0x20841, 0x20840, 0x01A10, 0x20842, 0x05080, 0x05081, 0x05082, 
	0x05083, 0x00300, 0x00301, 0x00302, 0x00303, 0x00304, 0x00305, 0x10060, 0x22080, 0x00308, 0x00309, 0x28800, 0x28801, 
	0x44402, 0x44403, 0x44400, 0x44401, 0x00310, 0x00311, 0x10C01, 0x10C00, 0x00314, 0x00315, 0x10070, 0x10C04, 0x00318, 
	0x00319, 0x28810, 0x10C08, 0x44412, 0x00000, 0x44410, 0x44411, 0x00320, 0x60400, 0x10044, 0x10045, 0x10042, 0x0C800, 
	0x10040, 0x10041, 0x06080, 0x06081, 0x06082, 0x06083, 0x1004A, 0x0C808, 0x10048, 0x10049, 0x58008, 0x08282, 0x08281, 
	0x08280, 0x10052, 0x0C810, 0x10050, 0x10051, 0x58000, 0x58001, 0x58002, 0x08288, 0x02A02, 0x02A03, 0x02A00, 0x02A01, 
	0x00340, 0x00341, 0x10024, 0x10025, 0x10022, 0x10023, 0x10020, 0x10021, 0x34001, 0x34000, 0x02601, 0x02600, 0x1002A, 
	0x34004, 0x10028, 0x10029, 0x0C400, 0x0C401, 0x21101, 0x21100, 0x60800, 0x60801, 0x10030, 0x10031, 0x0C408, 0x34010, 
	0x21109, 0x21108, 0x60808, 0x60809, 0x10038, 0x28420, 0x10006, 0x10007, 0x10004, 0x10005, 0x10002, 0x10003, 0x10000, 
	0x10001, 0x1000E, 0x40284, 0x1000C, 0x1000D, 0x1000A, 0x40280, 0x10008, 0x10009, 0x10016, 0x10017, 0x10014, 0x10015, 
	0x10012, 0x10013, 0x10010, 0x10011, 0x05104, 0x44802, 0x44801, 0x44800, 0x05100, 0x05101, 0x10018, 0x28400, 0x00380, 
	0x00381, 0x22005, 0x22004, 0x22003, 0x22002, 0x22001, 0x22000, 0x06020, 0x06021, 0x50101, 0x50100, 0x11800, 0x11801, 
	0x22009, 0x22008, 0x45001, 0x45000, 0x08221, 0x08220, 0x04902, 0x22012, 0x04900, 0x22010, 0x06030, 0x45008, 0x08229, 
	0x08228, 0x11810, 0x11811, 0x04908, 0x22018, 0x06008, 0x06009, 0x08211, 0x08210, 0x100C2, 0x22022, 0x100C0, 0x22020, 
	0x06000, 0x06001, 0x06002, 0x06003, 0x06004, 0x40240, 0x06006, 0x40242, 0x08203, 0x08202, 0x08201, 0x08200, 0x08207, 
	0x08206, 0x08205, 0x08204, 0x06010, 0x20900, 0x08209, 0x08208, 0x61002, 0x20904, 0x61000, 0x61001, 0x29020, 0x29021, 
	0x100A4, 0x22044, 0x100A2, 0x22042, 0x100A0, 0x22040, 0x20504, 0x40224, 0x0D005, 0x0D004, 0x20500, 0x40220, 0x0D001, 
	0x0D000, 0x03204, 0x18104, 0x08261, 0x08260, 0x03200, 0x18100, 0x03202, 0x18102, 0x11421, 0x11420, 0x00000, 0x11422, 
	0x03208, 0x18108, 0x0D011, 0x0D010, 0x29000, 0x29001, 0x10084, 0x04500, 0x10082, 0x40208, 0x10080, 0x10081, 0x06040, 
	0x40204, 0x06042, 0x40206, 0x40201, 0x40200, 0x10088, 0x40202, 0x29010, 0x08242, 0x08241, 0x08240, 0x10092, 0x40218, 
	0x10090, 0x10091, 0x11401, 0x11400, 0x11403, 0x11402, 0x40211, 0x40210, 0x10098, 0x40212, 0x00400, 0x00401, 0x00402, 
	0x00403, 0x00404, 0x00405, 0x00406, 0x00407, 0x00408, 0x00409, 0x0040A, 0x02140, 0x0040C, 0x0040D, 0x01091, 0x01090, 
	0x00410, 0x00411, 0x00412, 0x00413, 0x00414, 0x00860, 0x01089, 0x01088, 0x00418, 0x38000, 0x01085, 0x01084, 0x01083, 
	0x01082, 0x01081, 0x01080, 0x00420, 0x00421, 0x00422, 0x00423, 0x00424, 0x00850, 0x42080, 0x42081, 0x00428, 0x00429, 
	0x48801, 0x48800, 0x09100, 0x12200, 0x24401, 0x24400, 0x00430, 0x00844, 0x00432, 0x00846, 0x00841, 0x00840, 0x1C000, 
	0x00842, 0x00438, 0x0084C, 0x010A5, 0x010A4, 0x00849, 0x00848, 0x010A1, 0x010A0, 0x00440, 0x00441, 0x00442, 0x02108, 
	0x00444, 0x00830, 0x70001, 0x70000, 0x00448, 0x02102, 0x02101, 0x02100, 0x20280, 0x20281, 0x02105, 0x02104, 0x00450, 
	0x00824, 0x00452, 0x00826, 0x00821, 0x00820, 0x00823, 0x00822, 0x24802, 0x02112, 0x24800, 0x02110, 0x00829, 0x00828, 
	0x48400, 0x010C0, 0x00460, 0x00814, 0x04281, 0x04280, 0x00811, 0x00810, 0x00813, 0x00812, 0x54000, 0x54001, 0x02121, 
	0x02120, 0x00819, 0x00818, 0x0081B, 0x0081A, 0x00805, 0x00804, 0x41100, 0x00806, 0x00801, 0x00800, 0x00803, 0x00802, 
	0x0A080, 0x0080C, 0x0A082, 0x0080E, 0x00809, 0x00808, 0x0080B, 0x0080A, 0x00480, 0x00481, 0x00482, 0x00483, 0x00484, 
	0x14100, 0x42020, 0x01018, 0x00488, 0x00489, 0x01015, 0x01014, 0x20240, 0x01012, 0x01011, 0x01010, 0x00490, 0x00491, 
	0x0100D, 0x0100C, 0x0100B, 0x0100A, 0x01009, 0x01008, 0x40900, 0x01006, 0x01005, 0x01004, 0x01003, 0x01002, 0x01001, 
	0x01000, 0x004A0, 0x004A1, 0x42004, 0x04240, 0x42002, 0x42003, 0x42000, 0x42001, 0x30102, 0x30103, 0x30100, 0x30101, 
	0x4200A, 0x01032, 0x42008, 0x01030, 0x25000, 0x25001, 0x08501, 0x08500, 0x008C1, 0x008C0, 0x42010, 0x01028, 0x0A040, 
	0x0A041, 0x01025, 0x01024, 0x01023, 0x01022, 0x01021, 0x01020, 0x004C0, 0x49000, 0x04221, 0x04220, 0x20208, 0x20209, 
	0x08900, 0x08901, 0x20204, 0x20205, 0x02181, 0x02180, 0x20200, 0x20201, 0x20202, 0x01050, 0x0A028, 0x008A4, 0x0104D, 
	0x0104C, 0x008A1, 0x008A0, 0x01049, 0x01048, 0x0A020, 0x0A021, 0x01045, 0x01044, 0x20210, 0x01042, 0x01041, 0x01040, 
	0x04203, 0x04202, 0x04201, 0x04200, 0x00891, 0x00890, 0x42040, 0x04204, 0x0A010, 0x0A011, 0x01C00, 0x04208, 0x20220, 
	0x40500, 0x20222, 0x40502, 0x0A008, 0x00884, 0x04211, 0x04210, 0x00881, 0x00880, 0x00883, 0x00882, 0x0A000, 0x0A001, 
	0x0A002, 0x0A003, 0x0A004, 0x00888, 0x01061, 0x01060, 0x00500, 0x00501, 0x00502, 0x02048, 0x00504, 0x14080, 0x00506, 
	0x14082, 0x00508, 0x02042, 0x02041, 0x02040, 0x09020, 0x09021, 0x44200, 0x02044, 0x00510, 0x00511, 0x10A01, 0x10A00, 
	0x4A001, 0x4A000, 0x4A003, 0x4A002, 0x40880, 0x40881, 0x02051, 0x02050, 0x40884, 0x01182, 0x01181, 0x01180, 0x00520, 
	0x60200, 0x00522, 0x60202, 0x09008, 0x09009, 0x0900A, 0x0900B, 0x09004, 0x09005, 0x30080, 0x02060, 0x09000, 0x09001, 
	0x09002, 0x09003, 0x41042, 0x08482, 0x41040, 0x08480, 0x00941, 0x00940, 0x41044, 0x00942, 0x09014, 0x09015, 0x02C04, 
	0x08488, 0x09010, 0x09011, 0x02C00, 0x02C01, 0x00540, 0x0200A, 0x02009, 0x02008, 0x08882, 0x0200E, 0x08880, 0x0200C, 
	0x02003, 0x02002, 0x02001, 0x02000, 0x02007, 0x02006, 0x02005, 0x02004, 0x0C200, 0x0C201, 0x41020, 0x02018, 0x00921, 
	0x00920, 0x41024, 0x00922, 0x02013, 0x02012, 0x02011, 0x02010, 0x02017, 0x02016, 0x02015, 0x02014, 0x41012, 0x0202A, 
	0x41010, 0x02028, 0x26000, 0x00910, 0x10600, 0x10601, 0x02023, 0x02022, 0x02021, 0x02020, 0x09040, 0x40480, 0x02025, 
	0x02024, 0x41002, 0x00904, 0x41000, 0x41001, 0x00901, 0x00900, 0x41004, 0x00902, 0x4100A, 0x02032, 0x41008, 0x02030, 
	0x00909, 0x00908, 0x28201, 0x28200, 0x00580, 0x14004, 0x00582, 0x14006, 0x14001, 0x14000, 0x08840, 0x14002, 0x40810, 
	0x40811, 0x30020, 0x020C0, 0x14009, 0x14008, 0x01111, 0x01110, 0x40808, 0x40809, 0x08421, 0x08420, 0x14011, 0x14010, 
	0x01109, 0x01108, 0x40800, 0x40801, 0x40802, 0x01104, 0x40804, 0x01102, 0x01101, 0x01100, 0x03801, 0x03800, 0x30008, 
	0x08410, 0x14021, 0x14020, 0x42100, 0x42101, 0x30002, 0x30003, 0x30000, 0x30001, 0x09080, 0x40440, 0x30004, 0x30005, 
	0x08403, 0x08402, 0x08401, 0x08400, 0x08407, 0x08406, 0x08405, 0x08404, 0x40820, 0x40821, 0x30010, 0x08408, 0x40824, 
	0x01122, 0x01121, 0x01120, 0x08806, 0x0208A, 0x08804, 0x02088, 0x08802, 0x14040, 0x08800, 0x08801, 0x02083, 0x02082, 
	0x02081, 0x02080, 0x20300, 0x40420, 0x08808, 0x02084, 0x03404, 0x03405, 0x08814, 0x02098, 0x03400, 0x03401, 0x08810, 
	0x08811, 0x40840, 0x40841, 0x02091, 0x02090, 0x40844, 0x01142, 0x01141, 0x01140, 0x04303, 0x04302, 0x04301, 0x04300, 
	0x40409, 0x40408, 0x08820, 0x08821, 0x40405, 0x40404, 0x30040, 0x020A0, 0x40401, 0x40400, 0x40403, 0x40402, 0x41082, 
	0x08442, 0x41080, 0x08440, 0x00981, 0x00980, 0x41084, 0x00982, 0x0A100, 0x11200, 0x0A102, 0x11202, 0x40411, 0x40410, 
	0x40413, 0x40412, 0x00600, 0x00601, 0x00602, 0x00603, 0x00604, 0x00605, 0x00606, 0x00607, 0x00608, 0x05800, 0x0060A, 
	0x05802, 0x200C0, 0x12020, 0x44100, 0x44101, 0x00610, 0x00611, 0x10901, 0x10900, 0x51000, 0x51001, 0x51002, 0x10904, 
	0x00618, 0x05810, 0x01285, 0x01284, 0x51008, 0x01282, 0x01281, 0x01280, 0x00620, 0x60100, 0x040C1, 0x040C0, 0x12009, 
	0x12008, 0x21800, 0x21801, 0x12005, 0x12004, 0x12007, 0x12006, 0x12001, 0x12000, 0x12003, 0x12002, 0x00630, 0x00A44, 
	0x040D1, 0x040D0, 0x00A41, 0x00A40, 0x21810, 0x00A42, 0x12015, 0x12014, 0x00000, 0x12016, 0x12011, 0x12010, 0x12013, 
	0x12012, 0x00640, 0x00641, 0x040A1, 0x040A0, 0x20088, 0x20089, 0x2008A, 0x040A4, 0x20084, 0x20085, 0x19000, 0x02300, 
	0x20080, 0x20081, 0x20082, 0x20083, 0x0C100, 0x0C101, 0x21401, 0x21400, 0x00A21, 0x00A20, 0x00A23, 0x00A22, 0x20094, 
	0x20095, 0x19010, 0x21408, 0x20090, 0x20091, 0x20092, 0x28120, 0x04083, 0x04082, 0x04081, 0x04080, 0x00A11, 0x00A10, 
	0x10500, 0x04084, 0x200A4, 0x0408A, 0x04089, 0x04088, 0x200A0, 0x12040, 0x200A2, 0x12042, 0x00A05, 0x00A04, 0x04091, 
	0x04090, 0x00A01, 0x00A00, 0x00A03, 0x00A02, 0x05404, 0x00A0C, 0x28105, 0x28104, 0x05400, 0x00A08, 0x28101, 0x28100, 
	0x00680, 0x00681, 0x04061, 0x04060, 0x20048, 0x20049, 0x2004A, 0x04064, 0x20044, 0x20045, 0x50401, 0x50400, 0x20040, 
	0x20041, 0x20042, 0x01210, 0x68002, 0x68003, 0x68000, 0x68001, 0x04C02, 0x0120A, 0x04C00, 0x01208, 0x20054, 0x01206, 
	0x01205, 0x01204, 0x20050, 0x01202, 0x01201, 0x01200, 0x18800, 0x04042, 0x04041, 0x04040, 0x42202, 0x04046, 0x42200, 
	0x04044, 0x20064, 0x0404A, 0x04049, 0x04048, 0x20060, 0x12080, 0x20062, 0x12082, 0x18810, 0x04052, 0x04051, 0x04050, 
	0x4C009, 0x4C008, 0x42210, 0x04054, 0x20C01, 0x20C00, 0x20C03, 0x20C02, 0x4C001, 0x4C000, 0x01221, 0x01220, 0x2000C, 
	0x04022, 0x04021, 0x04020, 0x20008, 0x20009, 0x2000A, 0x04024, 0x20004, 0x20005, 0x20006, 0x04028, 0x20000, 0x20001, 
	0x20002, 0x20003, 0x2001C, 0x04032, 0x04031, 0x04030, 0x20018, 0x18400, 0x2001A, 0x18402, 0x20014, 0x20015, 0x20016, 
	0x01244, 0x20010, 0x20011, 0x20012, 0x01240, 0x04003, 0x04002, 0x04001, 0x04000, 0x20028, 0x04006, 0x04005, 0x04004, 
	0x20024, 0x0400A, 0x04009, 0x04008, 0x20020, 0x20021, 0x20022, 0x0400C, 0x04013, 0x04012, 0x04011, 0x04010, 0x00A81, 
	0x00A80, 0x04015, 0x04014, 0x0A200, 0x11100, 0x04019, 0x04018, 0x20030, 0x20031, 0x50800, 0x50801, 0x00700, 0x60020, 
	0x10811, 0x10810, 0x4400A, 0x60024, 0x44008, 0x44009, 0x44006, 0x02242, 0x44004, 0x02240, 0x44002, 0x44003, 0x44000, 
	0x44001, 0x0C040, 0x10802, 0x10801, 0x10800, 0x0C044, 0x10806, 0x10805, 0x10804, 0x23000, 0x23001, 0x10809, 0x10808, 
	0x44012, 0x44013, 0x44010, 0x44011, 0x60001, 0x60000, 0x60003, 0x60002, 0x60005, 0x60004, 0x10440, 0x10441, 0x60009, 
	0x60008, 0x44024, 0x6000A, 0x09200, 0x12100, 0x44020, 0x44021, 0x60011, 0x60010, 0x10821, 0x10820, 0x07003, 0x07002, 
	0x07001, 0x07000, 0x23020, 0x60018, 0x28045, 0x28044, 0x09210, 0x28042, 0x28041, 0x28040, 0x0C010, 0x0C011, 0x02209, 
	0x02208, 0x10422, 0x10423, 0x10420, 0x10421, 0x02203, 0x02202, 0x02201, 0x02200, 0x20180, 0x20181, 0x44040, 0x02204, 
	0x0C000, 0x0C001, 0x0C002, 0x10840, 0x0C004, 0x0C005, 0x0C006, 0x10844, 0x0C008, 0x0C009, 0x02211, 0x02210, 0x0C00C, 
	0x28022, 0x28021, 0x28020, 0x60041, 0x60040, 0x10404, 0x04180, 0x10402, 0x10403, 0x10400, 0x10401, 0x02223, 0x02222, 
    0x02221, 0x02220, 0x1040A, 0x28012, 0x10408, 0x28010, 0x0C020, 0x0C021, 0x41200, 0x41201, 0x00B01, 0x00B00, 0x10410, 
	0x28008, 0x11081, 0x11080, 0x28005, 0x28004, 0x28003, 0x28002, 0x28001, 0x28000, 0x52040, 0x14204, 0x22405, 0x22404, 
	0x14201, 0x14200, 0x22401, 0x22400, 0x20144, 0x20145, 0x44084, 0x022C0, 0x20140, 0x20141, 0x44080, 0x44081, 0x40A08, 
	0x10882, 0x10881, 0x10880, 0x14211, 0x14210, 0x1A008, 0x10884, 0x40A00, 0x40A01, 0x40A02, 0x01304, 0x1A002, 0x01302, 
	0x1A000, 0x01300, 0x60081, 0x60080, 0x04141, 0x04140, 0x60085, 0x60084, 0x104C0, 0x04144, 0x06400, 0x06401, 0x30200, 
	0x30201, 0x06404, 0x40640, 0x30204, 0x30205, 0x08603, 0x08602, 0x08601, 0x08600, 0x00000, 0x08606, 0x08605, 0x08604, 
	0x11041, 0x11040, 0x30210, 0x11042, 0x11045, 0x11044, 0x1A020, 0x01320, 0x52000, 0x52001, 0x04121, 0x04120, 0x20108, 
	0x20109, 0x08A00, 0x08A01, 0x20104, 0x20105, 0x02281, 0x02280, 0x20100, 0x20101, 0x20102, 0x20103, 0x0C080, 0x0C081, 
	0x0C082, 0x04130, 0x0C084, 0x06808, 0x08A10, 0x08A11, 0x11021, 0x11020, 0x11023, 0x11022, 0x20110, 0x06800, 0x20112, 
	0x06802, 0x04103, 0x04102, 0x04101, 0x04100, 0x10482, 0x04106, 0x10480, 0x04104, 0x11011, 0x11010, 0x04109, 0x04108, 
	0x20120, 0x40600, 0x20122, 0x40602, 0x11009, 0x11008, 0x22800, 0x04110, 0x1100D, 0x1100C, 0x22804, 0x04114, 0x11001, 
	0x11000, 0x11003, 0x11002, 0x11005, 0x11004, 0x28081, 0x28080)

def get_synd_1987(_pattern):
	aux = X18
	if _pattern >= X11:
		while _pattern & MASK8:
			while not (aux & _pattern):
				aux = aux >> 1
			_pattern ^= (aux / X11) * GENPOL
	return _pattern

def decode_2087(_data):
	code = (data[0] << 11) + (data[1] << 3) + (data[2] >> 5)
	syndrome = get_synd_1987(code)
	error_pattern = DECODING_TABLE_1987[syndrome]

	if error_pattern != 0x00:
		code ^= error_pattern

	return code >> 11

def encode_2087(_data):
    value = data[0]
    cksum = ENCODING_TABLE_2087[value]
    data[1] = cksum & 0xFF
    data[2] = cksum >> 8
    return _data


#------------------------------------------------------------------------------
# Used to execute the module directly to run built-in tests
#------------------------------------------------------------------------------

if __name__ == '__main__':
    
    from binascii import b2a_hex as h
    from time import time