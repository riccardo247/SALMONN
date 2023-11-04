# Copyright (2023) Tsinghua University, Bytedance Ltd. and/or its affiliates
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import argparse
from model import SALMONN
       
if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--device", type=str, default="cuda:0")
    parser.add_argument("--ckpt_path", type=str, default=None)
    parser.add_argument("--whisper_path", type=str, default=None)
    parser.add_argument("--beats_path", type=str, default=None)
    parser.add_argument("--vicuna_path", type=str, default=None)
    parser.add_argument("--wav_base_dir", type=str, default=None)
    parser.add_argument("--low_resource", action='store_true', default=False)
    parser.add_argument("--debug", action="store_true", default=False)

    args = parser.parse_args()

    model = SALMONN(
        ckpt=args.ckpt_path,
        whisper_path=args.whisper_path,
        beats_path=args.beats_path,
        vicuna_path=args.vicuna_path,
        low_resource=args.low_resource
    )
    model.to(args.device)
    model.eval()
  
# Base directory path
wav_base_dir = args.wav_base_dir

# Recursively iterate through all directories and files
for root, _, files in os.walk(wav_base_dir):
    # Split the directory path into parts
    path_parts = root.split(os.path.sep)
    
    # Check if the directory structure is valid (name/name structure)
    if len(path_parts) >= 3 and path_parts[-1] == path_parts[-2]:
        for file_name in files:
            if file_name.endswith(".wav"):
                wav_file_path = os.path.join(root, file_name)
                try:
                  text = process() model.generate(wav_file_path, prompt=prompt)[0]
                except Exception as e:
                  text = ""
                # Create a directory for the TXT files (if not exists)
                txt_dir = os.path.join(root + "_voicetxt")
                os.makedirs(txt_dir, exist_ok=True)

                # Construct the output TXT file path
                txt_file_name = os.path.splitext(file_name)[0] + ".txt"
                txt_file_path = os.path.join(txt_dir, txt_file_name)

                # Save the processed text into the TXT file
                with open(txt_file_path, "w") as txt_file:
                    txt_file.write(text)

                print(f"Processed and saved '{wav_file_path}' to '{txt_file_path}'")  
