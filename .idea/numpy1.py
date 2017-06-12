import numpy as np
from numpy import fft
samples = (1, 1640, 3281, 4899, 6506, 8083, 9627, 11141, 12600, 14021, 15375, 16681, 17909, 19079, 20164, 21174, 22105, 22936, 23695, 24346, 24907, 25374, 25731, 25999, 26156, 26215, 26168, 26020, 25770, 25417, 24966, 24416, 23769, 23034, 22198, 21287, 20282, 19205, 18048, 16821, 15530, 14175, 12767, 11305, 9804, 8259, 6688, 5082, 3466, 1826, 188, -1456, -3092, -4719, -6322, -7907, -9453, -10971, -12437, -13861, -15226, -16533, -17777, -18947, -20045, -21065, -21999, -22852, -23609, -24278, -24850, -25322, -25700, -25970, -26146, -26212, -26179, -26042, -25804, -25461, -25024, -24481, -23851, -23117, -22302, -21391, -20403, -19331, -18181, -16967, -15677, -14333, -12929, -11475, -9975, -8439, -6864, -5269, -3648, -2015, -372, 1266, 2912, 4528, 6147, 7724, 9282, 10799, 12273, 13701, 15075, 16387, 17639, 18817, 19925, 20953, 21897, 22760, 23527, 24207, 24790, 25273, 25663, 25943, 26134, 26204, 26195, 26057, 25839, 25505, 25077, 24550, 23924, 23208, 22397, 21501, 20519, 19454, 18320, 17103, 15832, 14485, 13093, 11641, 10150, 8611, 7050, 5445, 3838, 2197, 563, -1085, -2719, -4352, -5959, -7550, -9104, -10630, -12107, -13542, -14922, -16240, -17501, -18687, -19802, -20842, -21792, -22668, -23444, -24134, -24729, -25224, -25622, -25919, -26113, -26208, -26193, -26086, -25863, -25551, -25131, -24612, -24004, -23290, -22497, -21605, -20634, -19582, -18449, -17249, -15975, -14645, -13250, -11813, -10317, -8792, -7225, -5633, -4017, -2389, -744, 893, 2538, 4165, 5778, 7370, 8930, 10457, 11944, 13380, 14767, 16097, 17356, 18560, 19677, 20728, 21689, 22572, 23361, 24061, 24664, 25175, 25580, 25892, 26096, 26200, 26203, 26101, 25894, 25592, 25182, 24678, 24076, 23378, 22589, 21713, 20747, 19707, 18580, 17390, 16122, 14800, 13412, 11977, 10491, 8966, 7405, 5815, 4201, 2576, 931, -707, -2353, -3979, -5597, -7188, -8757, -10285, -11776, -13221, -14611, -15949, -17218, -18425, -19554, -20614, -21583, -22476, -23276, -23985, -24603, -25119, -25540, -25862, -26076, -26197, -26205, -26118, -25924, -25630, -25235, -24739, -24151, -23459, -22687, -21814, -20862, -19829, -18711, -17530, -16270, -14951, -13575, -12139, -10666, -9138, -7585, -5998, -4384, -2762, -1117, 521, 2165, 3795, 5415, 7009, 8580, 10112, 11611, 13056, 14460, 15796, 17080, 18290, 19430, 20497, 21477, 22380, 23189, 23909, 24538, 25064, 25501, 25825, 26063, 26183, 26212, 26133, 25951, 25668, 25287, 24798, 24223, 23544, 22777, 21919, 20975, 19949, 18843, 17667, 16416, 15105, 13733, 12306, 10835, 9313, 7765, 6177, 4571, 2945, 1305, -334, -1979, -3611, -5230, -6833, -8398, -9945, -11438, -12898, -14301, -15649, -16936, -18156, -19306, -20377, -21373, -22278, -23104, -23833, -24468, -25014, -25450, -25799, -26037, -26177, -26214, -26146, -25977, -25706, -25334, -24860, -24292, -23627, -22867, -22024, -21083, -20072, -18971, -17805, -16561, -15259, -13890, -12471, -11004, -9489, -7941, -6361, -4752, -3132, -1493, 151, 1790, 3427, 5047, 6650, 8224, 9770, 11271, 12734, 14144, 15499, 16794, 18019, 19180, 20259, 21263, 22183, 23010, 23757, 24401, 24955, 25409, 25760, 26019, 26163, 26218, 26157, 26002, 25742, 25380, 24920, 24362, 23705, 22962, 22119, 21198, 20189, 19101, 17941, 16706, 15408, 14051, 12633, 11174, 9663, 8118, 6543, 4935, 3318, 1677, 39, -1606, -3240, -4865, -6469, -8047, -9594, -11105, -12569, -13987, -15349, -16646, -17889, -19047, -20143, -21153, -22081, -22923, -23676, -24331, -24899, -25361, -25727, -25993, -26152, -26218, -26166, -26030, -25771, -25431, -24974, -24431, -23786, -23048, -22222, -21305, -20309, -19228, -18076, -16850, -15559, -14206, -12801, -11337, -9841, -8292, -6725, -5119, -3502, -1864, -225, 1418, 3057, 4678, 6291, 7866, 9424, 10931, 12409, 13825, 15199, 16502, 17751, 18918, 20025, 21039, 21983, 22830, 23595, 24262, 24840, 25311, 25694, 25963, 26145, 26210, 26182, 26046, 25810, 25470, 25036, 24493, 23868, 23133, 22323, 21412, 20427, 19355, 18209, 16995, 15707, 14365, 12960, 11509, 10010, 8473, 6902, 5304, 3684, 2055, 408, -1230, -2872, -4496, -6105, -7693, -9244, -10768, -12237, -13672, -15042, -16360, -17609, -18794, -19898, -20932, -21876, -22741, -23512, -24191, -24779, -25261, -25658, -25937, -26129, -26208, -26190, -26067, -25843, -25512, -25092, -24558, -23945, -23221, -22419, -21520, -20544, -19478, -18347, -17132, -15860, -14519, -13123, -11675, -10185, -8646, -7085, -5486, -3868, -2241, -595, 1043, 2686, 4312, 5925, 7513, 9069, 10596, 12073, 13512, 14888, 16214, 17471, 18661, 19779, 20815, 21777, 22644, 23431, 24117, 24717, 25214, 25614, 25914, 26109, 26207, 26195, 26089, 25870, 25558, 25142, 24625, 24019, 23308, 22514, 21629, 20655, 19607, 18476, 17276, 16007, 14674, 13283, 11846, 10351, 8829, 7258, 5671, 4055, 2423, 786, -861, -2497, -4130, -5741, -7333, -8897, -10422, -11910, -13349, -14735, -16067, -17330, -18532, -19653, -20705, -21668, -22553, -23343, -24047, -24652, -25162, -25575, -25883, -26095, -26197, -26206, -26101, -25905, -25596, -25195, -24689, -24091, -23395, -22609, -21732, -20772, -19728, -18611, -17413, -16157, -14825, -13448, -12009, -10524, -9003, -7439, -5852, -4240, -2610, -970, 671, 2315, 3941, 5562, 7152, 8721, 10250, 11745, 13186, 14583, 15917, 17190, 18398, 19532, 20586, 21567, 22453, 23260, 23972, 24586, 25112, 25529, 25857, 26073, 26194, 26207, 26120, 25931, 25636, 25246, 24752, 24163, 23479, 22703, 21835, 20887, 19850, 18740, 17556, 16299, 14984, 13604, 12175, 10698, 9173, 7624, 6030, 4424, 2797, 1155, -483, -2127, -3761, -5375, -6976, -8542, -10079, -11577, -13025, -14426, -15770, -17048, -18264, -19407, -20471, -21459, -22357, -23173, -23894, -24524, -25055, -25489, -25822, -26055, -26186, -26208, -26140, -25952, -25680, -25292, -24814, -24234, -23563, -22794, -21940, -20997, -19973, -18870, -17693, -16446, -15136, -13764, -12340, -10868, -9348, -7801, -6213, -4608, -2982, -1343, 299, 1938, 3578, 5191, 6797, 8364, 9908, 11407, 12865, 14268, 15621, 16906, 18130, 19280, 20353, 21353, 22258, 23085, 23818, 24455, 25001, 25445, 25788, 26036, 26173, 26215, 26148, 25983, 25712, 25344, 24872, 24306, 23642, 22888, 22039, 21112, 20088, 19006, 17824, 16597, 15282, 13927, 12502, 11038, 9524, 7976, 6397, 4790, 3168, 1530, -112, -1755, -3388, -5012, -6612, -8191, -9733, -11239, -12701, -14111, -15472, -16762, -17995, -19153, -20234, -21245, -22158, -22998, -23736, -24390, -24943, -25398, -25758, -26007, -26169, -26210, -26166, -26001, -25754, -25385, -24936, -24371, -23725, -22977, -22140, -21221, -20210, -19130, -17966, -16735, -15439, -14081, -12669, -11204, -9700, -8152, -6580, -4973, -3352, -1717, -75, 1569, 3202, 4829, 6432, 8011, 9561, 11071, 12534, 13959, 15313, 16624, 17856, 19025, 20118, 21130, 22062, 22904, 23659, 24320, 24885, 25351, 25721, 25987, 26151, 26217, 26168, 26033, 25780, 25439, 24986, 24444, 23800, 23068, 22240, 21329, 20330, 19255, 18102, 16880, 15587, 14241, 12829, 11376, 9871, 8331, 6759, 5157, 3537, 1905, 258, -1377, -3022, -4641, -6254, -7831, -9389, -10898, -12373, -13798, -15163, -16479, -17718, -18896, -19999, -21017, -21963, -22811, -23579, -24249, -24825, -25305, -25684, -25960, -26141, -26209, -26186, -26047, -25820, -25478, -25044, -24512, -23876, -23157, -22339, -21434, -20452, -19378, -18238, -17021, -15739, -14394, -12996, -11540, -10045, -8510, -6935, -5343, -3722, -2088, -450, 1195, 2835, 4457, 6073, 7652, 9214, 10729, 12209, 13637, 15011, 16333, 17580, 18768, 19874, 20908, 21858, 22720, 23497, 24175, 24767, 25254)
print fft.rfftfreq(1024, d=1/44100.0)