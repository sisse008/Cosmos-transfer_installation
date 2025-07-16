



https://docs.nvidia.com/cosmos/latest/transfer/installation.html

- clone cosmos-transfer repository
- create environment
- install dependencies


-running script.py will setup the needed environment for running inference cosmos-transfer1. NOT TRAINING!

-need to first create a hugging face access token with read permission @ https://huggingface.co/settings/tokens.

-The model weights (downloaded from huggingface) require about 300GB of free storage. Not all checkpoints will be used in every generation.

-in order to test run, need to first download the mp4 file from https://docs.nvidia.com/cosmos/latest/_static/transfer1-edge-detect.mp4 and place in folder "assets"


system requirements:

https://docs.nvidia.com/cosmos/latest/prerequisites.html#prerequisites
https://github.com/nvidia-cosmos/cosmos-transfer1/blob/main/INSTALL.md


- Ubuntu: 24.04, 22.04, or 20.04
- Python: 3.12.x with Conda installed
- NVIDIA Container Toolkit: 1.16.2 or later
- CUDA: 12.4 or later

- CPU Memory: At least 90GB of RAM is required.
- CPU: Currently, only x86_64 architecture is supported.




there are two types of environment setups for running inference. one with conda and the other with docker. we will use conda.