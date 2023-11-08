import os
import subprocess
import sys
#from AudioDB.ProcessAudio import EngineSteam
# Specify the base directory path

# Create an empty dictionary to store WAV files and their corresponding directory structure
wav_files = {}
#es = EngineSteam()


def change_extension(file_path, new_extension):
    """

    :param file_path: inout file complete path or filename with ext
    :param new_extension: new ext
    :return: filename with new extension. e.g. chunk0.wav
    """
    # Split the filename into name and extension
    base_name = os.path.splitext(file_path)[0]
    # Return the base name with the new extension
    return f"{base_name}.{new_extension}"
  
def convert_to_wav(input_path, output_path=None):
    """
    convert any audio format to wav with ffmpeg
    :param input_path: inout music file
    :param output_file: output path with ext
    :return:
    """
    try:
        command = [
            "ffmpeg",
            "-i", input_path,
            "-acodec", "pcm_s16le",
            "-ar", "48000",
            output_path
        ]
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError:
        print(f"Error converting {input_path} to {output_path}")
    except FileNotFoundError:
        print("FFmpeg not found. Ensure it's installed and in your system's PATH.")
      
# Function to search for WAV files and associate them with TXT files and their directory structure
def find_wav_files(directory, prefix=""):
    for root, dirs, files in os.walk(directory):
      path_parts = root.split(os.path.sep)
      #print(f"{root}")
      for thisfile in files:
        print(f"{thisfile}")
        if thisfile.lower().startswith("chunk") and thisfile.lower().endswith(".mp3") and path_parts[-1] ==path_parts[-2]:
          
          mp3_file_path = os.path.join(root, thisfile)
          wav_filename = change_extension(thisfile, "wav")
          wav_file_path = os.path.join(root, wav_filename)
          if not os.path.exists(wav_file_path):
            convert_to_wav(mp3_file_path, wav_file_path)
          txt_file_path = os.path.join(os.path.sep.join(path_parts[:-1]), path_parts[-1]+"_txt", thisfile.split(".")[0] + ".txt")
          #print(f"txt file is: {txt_file_path}")
          #get voice description as well
          if os.path.exists(txt_file_path):
              wav_files[txt_file_path] = (wav_file_path ,prefix + root)


def main(base_path, output_path):
  # Call the function to search for WAV files and associate them with TXT files
  find_wav_files(base_path)
  print(f"found {len(wav_files)} chunk files")
  # Print the results
  with open(output_path, 'w') as f:
    for txt_file, item in wav_files.items():
        wav_file, dir_path = item
        f.write(f"{wav_file}|{txt_file}|{dir_path} \n"  )
        #print("TXT File:", txt_file)
      
if __name__ == '__main__':
    if len(sys.argv) == 3:
        base_path = sys.argv[1]
        output_path = sys.argv[2]
        main(base_path, output_path)
    else:
       print("required base_path (audio files /finetune/audio ) and output_path (output for txt file /finetune)")
