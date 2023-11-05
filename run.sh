#!/bin/bash

nohup python3 process_files.py --ckpt_path /salmonn/ckpt/salmonn_v1.pth --whisper_path /salmonn/whisper --beats_path /salmonn/beats/BEATs_iter3_plus_AS2M_finetuned_on_AS2M_cpt2.pt --vicuna_path /salmonn/vicuna/ --wav_base_dir /root/ >../log_salmon.txt 2>&1 &
