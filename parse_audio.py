import numpy as np
import tensorflow as tf
import struct
import os

def Audio_data_parse(file_path):

    with open(file_path, 'rb') as wav_file:
              #Get main header
              chunk_id = wav_file.read(4)
              assert chunk_id == b'RIFF' # RIFF:little endian

              chunk_size = struct.unpack('<I', wav_file.read(4))[0] #struct.unpack converts 4bytes data into an integer

              wav_format = wav_file.read(4)
              assert wav_format == b'WAVE', wav_format

              # Sub Chunk 1
              sub_chunk_1_id = wav_file.read(4)
              assert sub_chunk_1_id == b'fmt ', sub_chunk_1_id

              sub_chunk_1_size = struct.unpack('<I', wav_file.read(4))[0]

              audio_format = struct.unpack('<H', wav_file.read(2))[0]
              assert audio_format == 1, '1 == PCM Format: assumed PCM'

              num_channels = struct.unpack('<H', wav_file.read(2))[0]
              assert num_channels == 1, '1 == Mono, 2 == Stereo: assumed Mono'

              sample_rate = struct.unpack('<I', wav_file.read(4))[0]
              assert sample_rate == 16000, 'assumed 16000'

              byte_rate = struct.unpack('<I', wav_file.read(4))[0]
              assert byte_rate == 32000, byte_rate

              # Could this be something other than an int?
              block_align = struct.unpack('<H', wav_file.read(2))[0]
              assert block_align == 2, block_align

              bits_per_sample = struct.unpack('<H', wav_file.read(2))[0]
              assert bits_per_sample == 16, bits_per_sample

              # Sub Chunk 2
              sub_chunk_2_id = wav_file.read(4)
              assert sub_chunk_2_id == b'data', sub_chunk_2_id

              sub_chunk_2_size = struct.unpack('<I', wav_file.read(4))[0]

              samples = []
              bytes_per_sample = bits_per_sample / 8
              assert (sub_chunk_2_size % bytes_per_sample) == 0, 'Uneven sample size'

              sample_count = int(sub_chunk_2_size / bytes_per_sample)

              for _ in range(sample_count):
                  samples.append(struct.unpack('<h', wav_file.read(2))[0])

              assert chunk_size == (
                      len(wav_format) +
                      len(sub_chunk_1_id) + sub_chunk_1_size + 4 +  # Full size of subchunk 1
                      len(sub_chunk_2_id) + sub_chunk_2_size + 4 # Full size of subchunk 2
                  ), chunk_size

              assert sub_chunk_1_size == (
                      2 +  # audio_format
                      2 +  # num_channels
                      4 +  # sample_rate
                      4 +  # byte_rate
                      2 +  # block_align
                      2  # bits_per_sample
                  ), sub_chunk_1_size

              bytes_per_sample = bits_per_sample / 8
              assert byte_rate == (sample_rate * num_channels * bytes_per_sample), byte_rate

              assert block_align == (num_channels * bytes_per_sample), block_align
     
              assert sub_chunk_2_size == (len(samples) * bytes_per_sample), sub_chunk_2_size

              length_in_seconds = (len(samples) / sample_rate)

    return samples, length_in_seconds, sample_count
