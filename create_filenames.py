import csv

csvdata = [
    [
        "output_filename",       # filename to be saved
        "source_number",         # number of audio sources, 1~4 in this case
        "s1_path",               # filepath of the 1st source
        "s1_start",              # the start time of the 1st source (used to crop and extract segment)
        "s1_end",                # the end time of the 1st source (used to crop and extract segment), set the duration *(s1_end - s1_start) between 3~10 seems realistic
        "s1_tag",                # the start time of the 1st source in the simulated data (used for mixture)
        "s1_snr",                # the snr the 1st source in the simulated data (used for mixture), set random values in -3.0~3.0
        "s1_text",               # the text (or label) the 1st source
        "s1_imagepath1",         # the 1st image filepath of the 1st source
        "s1_imagepath2",         # the 2nd image filepath of the 1st source
        "s1_imagepath3",         # the 3rd image filepath of the 1st source
        "s1_imagepath4",         # the 4th image filepath of the 1st source
        "s1_imagepath5",         # the 5th image filepath of the 1st source
        "s2_path",
        "s2_start",
        "s2_end",
        "s2_tag",
        "s2_snr",
        "s2_text",
        "s2_imagepath1", 
        "s2_imagepath2",
        "s2_imagepath3",
        "s2_imagepath4",
        "s2_imagepath5",
        "s3_path",
        "s3_start",
        "s3_end",
        "s3_tag",
        "s3_snr",
        "s3_text",
        "s3_imagepath1", 
        "s3_imagepath2",
        "s3_imagepath3",
        "s3_imagepath4",
        "s3_imagepath5",
        "s4_path",
        "s4_start",
        "s4_end",
        "s4_tag",
        "s4_snr",
        "s4_text",
        "s4_imagepath1", 
        "s4_imagepath2",
        "s4_imagepath3",
        "s4_imagepath4",
        "s4_imagepath5",
    ]
]

# an example
csvdata.append([
    '1.wav',
    3,
    '/export/corpora7/HW/LibriMix/Libri2Mix/wav16k/min/test/s1/1089-134686-0004_1284-1180-0027.wav',
    0.1,
    2.0,
    3.0,
    2.42,
    'speech',
    '/path1',
    '/path2',
    '/path3',
    '/path4',
    '/path5',
    '/export/corpora7/HW/LibriMix/Libri2Mix/wav16k/min/test/s1/1188-133604-0005_6829-68769-0036.wav',
    1.0,
    4.2,
    1.3,
    -1.4,
    'speech',
    '/path1',
    '/path2',
    '/path3',
    '/path4',
    '/path5',
    '/export/corpora7/HW/LibriMix/Libri2Mix/wav16k/min/test/s1/121-121726-0003_1089-134691-0014.wav',
    0.8,
    2.5,
    6.2,
    0.5,
    'speech',
    '/path1',
    '/path2',
    '/path3',
    '/path4',
    '/path5',
    '/export/corpora7/HW/LibriMix/Libri2Mix/wav16k/min/test/s1/1320-122617-0035_121-121726-0009.wav',
    2.5,
    5.2,
    5.0,
    -1.3,
    'speech',
    '/path1',
    '/path2',
    '/path3',
    '/path4',
    '/path5',
    ])
        
file_path = 'vggsound_mix_test.csv'
# Writing to the CSV file
with open(file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(csvdata)
print(f'Data has been written to {file_path}')
