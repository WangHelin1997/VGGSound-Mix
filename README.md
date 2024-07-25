# Generating the VGGSound-Mix dataset

This script supports generating multiple-source mixture audio for training with the VGG-Sound dataset, which can be served as training materials for audio source separation, sound event detection, audio tagging and target sound extraction.


## Python requirements

Requires python 3.8, and the numpy, scipy, and pandas packages
```sh
$ pip install -r requirements.txt
```

## Prerequisites

This requires the [VGG-Sound](https://www.robots.ox.ac.uk/~vgg/data/vggsound/) dataset.

## Creating LibriLight-Mix

### Creating meta files

```sh
$ python create_filenames.py 
```

### Creating mixture files

```sh
$ python create_vggsoundmix.py \
    --output-dir ./debug/ \
    --sr 24000 \
    --fixed-len 10
 
```

The arguments for the script are:
* **output-dir**: Where to write the new dataset.
* **sr**: Sampling rate.
* **fixed-len**: The duration of audio file to simulate. 


## Output data organization

For each utterance in the training (tr) set folder, the following wav files are written:

1. s1: isolated data from source 1
2. s2: isolated data from source 2
3. s3: isolated data from source 3
4. s4: isolated data from source 4
5. mix: mixture audio for N speakers, contains mixture of s1, s2, ..., sN.

## Reference

https://wham.whisper.ai/WHAMR_README.html
