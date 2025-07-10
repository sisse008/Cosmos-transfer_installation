#!/usr/bin/env python3

import subprocess
import os
import sys


def run(cmd, **kwargs):
    print(f"➡️ Running: {cmd}")
    subprocess.run(cmd, shell=True, check=True, **kwargs)


'''

https://docs.nvidia.com/cosmos/latest/transfer/installation.html

- clone cosmos-transfer repository
- create environment
- install dependencies
'''
def installation():
    repo = "git@github.com:nvidia-cosmos/cosmos-transfer1.git"

    try:
        run(f"git clone {repo}")  # will clone into location of pycharm project
    except subprocess.CalledProcessError:
        print("Repository already exists—skipping clone.")

    os.chdir("cosmos-transfer1")  # change directory into cosmos-transfer1

    run("git submodule update --init --recursive")

    # Create the cosmos-transfer1 conda environment.
    run(f"conda env create --file cosmos-transfer1.yaml")

    # ⚠️ From here on, we must run inside the activated conda env (one run command so run all in the same shell)
    bash_commands = """
      source ~/.bashrc
      conda activate cosmos-transfer1 &&
    
      echo "🔁 Activating environment: cosmos-transfer1" &&
    
      # Install the dependencies.
      pip install -r requirements.txt &&
    
      # Patch Transformer engine linking issues in conda environments.
      conda_prefix=$CONDA_PREFIX
      if [ -z "$conda_prefix" ]; then
          echo "⚠️  CONDA_PREFIX not found. Ensure 'conda activate' worked."
      else
          ln -sf $conda_prefix/lib/python3.10/site-packages/nvidia/*/include/* $conda_prefix/include/ &&
          ln -sf $conda_prefix/lib/python3.10/site-packages/nvidia/*/include/* $conda_prefix/include/python3.10
      fi &&
    
      # Install Transformer engine.
      pip install transformer-engine[pytorch]==1.12.0 &&
    
      # Validate installation
      CUDA_HOME=$CONDA_PREFIX PYTHONPATH=$(pwd) python scripts/test_environment.py
      """

    run(f'bash -l -c "{bash_commands}"')

    print("\n✅ Installation complete! You can proceed with the Quickstart guide.")


'''
need to first download the mp4 file from https://docs.nvidia.com/cosmos/latest/_static/transfer1-edge-detect.mp4 and place in folder "assets"
'''
def generate_visual_simulation_from_video_source():
    bash_commands = r'''
          source ~/.bashrc
          conda activate cosmos-transfer1 &&

          echo "🎬 Generating visual simulation from source video..."

          export CUDA_VISIBLE_DEVICES=0
          export CHECKPOINT_DIR="${CHECKPOINT_DIR:=./checkpoints}"

          CUDA_HOME=$CONDA_PREFIX PYTHONPATH=$(pwd) python cosmos_transfer1/diffusion/inference/transfer.py \
            --checkpoint_dir "$CHECKPOINT_DIR" \
            --video_save_folder outputs/example1_single_control_edge \
            --controlnet_specs assets/inference_cosmos_transfer1_single_control_edge.json \
            --offload_text_encoder_model
        '''

    run(f'bash -l -c "{bash_commands}"')
    print("\n✅ Visual simulation generated! Check `outputs/example1_single_control_edge`.")


'''

https://docs.nvidia.com/cosmos/latest/transfer/quickstart_guide.html

- need to first create a hugging face access token with read permission @ https://huggingface.co/settings/tokens
******The model weights require about 300GB of free storage. Not all checkpoints will be used in every generation.******
'''

def quickstart():
    bash_commands = """
      source ~/.bashrc
      conda activate cosmos-transfer1 &&

      echo "🔑 Logging into Hugging Face..." &&
      huggingface-cli login &&

      echo "⏬ Downloading diffusion model checkpoints (~300 GB)..." &&
      CUDA_HOME=$CONDA_PREFIX PYTHONPATH=$(pwd) \
      python scripts/download_diffusion_checkpoints.py \
          --model_sizes 7B --model_types Text2World
    """

    run(f'bash -l -c "{bash_commands}"')

    print("\n✅ Quickstart complete! Model is downloaded and ready to use.")
    generate_visual_simulation_from_video_source()

def main():
    installation()
    quickstart()



if __name__ == "__main__":
    main()
