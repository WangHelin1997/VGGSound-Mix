import os
import numpy as np
import soundfile as sf
import pandas as pd
import argparse
from utils import read_scaled_wav, quantize, fix_length, create_mixes
import multiprocessing
import random

FILELIST_STUB = 'vggsound_mix_{}.csv'

MIX_DIR = 'mix_dir'
S1_DIR = 's1'
S2_DIR = 's2'
S3_DIR = 's3'
S4_DIR = 's4'
SPLITS = ['test']

def create_one(i_utt, output_name, vggsoundmix_df, SAMPLE_RATES, output_root, splt, FIXED_LEN):
    wav_dir = 'wav' + str(SAMPLE_RATES)
    output_path = os.path.join(output_root, wav_dir, splt)
    if not os.path.exists(os.path.join(output_path, MIX_DIR, output_name)):
        utt_row = vggsoundmix_df[vggsoundmix_df['output_filename'] == output_name]
        source_number = utt_row['source_number'].iloc[0]

        s1_path = utt_row['s1_path'].iloc[0]
        s2_path = utt_row['s2_path'].iloc[0]
        s3_path = utt_row['s3_path'].iloc[0]
        s4_path = utt_row['s4_path'].iloc[0]

        s1_start = float(utt_row["s1_start"].iloc[0])
        s1_end = float(utt_row["s1_end"].iloc[0])
        s1_tag = float(utt_row["s1_tag"].iloc[0])
        s1_snr = 10**(float(utt_row["s1_snr"].iloc[0]) / 20)

        s2_start = float(utt_row["s2_start"].iloc[0])
        s2_end = float(utt_row["s2_end"].iloc[0])
        s2_tag = float(utt_row["s2_tag"].iloc[0])
        s2_snr = 10**(float(utt_row["s2_snr"].iloc[0]) / 20)

        s3_start = float(utt_row["s3_start"].iloc[0])
        s3_end = float(utt_row["s3_end"].iloc[0])
        s3_tag = float(utt_row["s3_tag"].iloc[0])
        s3_snr = 10**(float(utt_row["s3_snr"].iloc[0]) / 20)

        s4_start = float(utt_row["s4_start"].iloc[0])
        s4_end = float(utt_row["s4_end"].iloc[0])
        s4_tag = float(utt_row["s4_tag"].iloc[0])
        s4_snr = 10**(float(utt_row["s4_snr"].iloc[0]) / 20)


        snr_ratio = 0.9/(s1_snr + s2_snr + s3_snr + s4_snr) # avoid out-of-range
        s1 = quantize(read_scaled_wav(s1_path, s1_snr*snr_ratio, s1_start, s1_end, SAMPLE_RATES))
        s2 = quantize(read_scaled_wav(s2_path, s2_snr*snr_ratio, s2_start, s2_end, SAMPLE_RATES))
        s3 = quantize(read_scaled_wav(s3_path, s3_snr*snr_ratio, s3_start, s3_end, SAMPLE_RATES))
        s4 = quantize(read_scaled_wav(s4_path, s4_snr*snr_ratio, s4_start, s4_end, SAMPLE_RATES))
        s1, s2, s3, s4 = fix_length(s1, s2, s3, s4, s1_tag, s2_tag, s3_tag, s4_tag, FIXED_LEN, SAMPLE_RATES)
    
        mix = create_mixes(source_number, s1, s2, s3, s4)

        # write audio
        sf.write(os.path.join(output_path, MIX_DIR, output_name), mix, SAMPLE_RATES, subtype='FLOAT')
        if source_number > 0:
            sf.write(os.path.join(output_path, S1_DIR, output_name), s1, SAMPLE_RATES, subtype='FLOAT')
        if source_number > 1:
            sf.write(os.path.join(output_path, S2_DIR, output_name), s2, SAMPLE_RATES, subtype='FLOAT')
        if source_number > 2:
            sf.write(os.path.join(output_path, S3_DIR, output_name), s3, SAMPLE_RATES, subtype='FLOAT')
        if source_number > 3:
            sf.write(os.path.join(output_path, S4_DIR, output_name), s4, SAMPLE_RATES, subtype='FLOAT')

    
        if (i_utt + 1) % 500 == 0:
            print('Completed {} of {} utterances'.format(i_utt + 1, len(vggsoundmix_df)))
                    
                
def create_wham(args, output_root):
    FIXED_LEN = args.fixed_len
    SAMPLE_RATES = args.sr

    for splt in SPLITS:

        vggsoundmix_path = FILELIST_STUB.format(splt)
        vggsoundmix_df = pd.read_csv(vggsoundmix_path)

        wav_dir = 'wav' + str(SAMPLE_RATES)
        output_path = os.path.join(output_root, wav_dir, splt)
        os.makedirs(os.path.join(output_path, MIX_DIR), exist_ok=True)
        os.makedirs(os.path.join(output_path, S1_DIR), exist_ok=True)
        os.makedirs(os.path.join(output_path, S2_DIR), exist_ok=True)
        os.makedirs(os.path.join(output_path, S3_DIR), exist_ok=True)
        os.makedirs(os.path.join(output_path, S4_DIR), exist_ok=True)

        utt_ids = vggsoundmix_df['output_filename']

        cmds = []
        for i_utt, output_name in enumerate(utt_ids):
            cmds.append((i_utt, output_name, vggsoundmix_df, SAMPLE_RATES, output_root, splt, FIXED_LEN))
        print('Totally {} utterances'.format(len(cmds)))
        random.shuffle(cmds) # For parallel CPU processing, which can run several scripts at the same time.
        with multiprocessing.Pool(processes=50) as pool:
            pool.starmap(create_one, cmds)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output-dir', type=str, default='./debug/',
                        help='Output directory for writing datasets.')
    parser.add_argument('--sr', type=int, default=24000,
                help='Sampling rate')
    parser.add_argument('--fixed-len', type=float, default=10,
            help='Fixed length of simulated audio')

    args = parser.parse_args()
    print('All arguments:', args)
    os.makedirs(args.output_dir, exist_ok=True)
    create_wham(args, args.output_dir)
