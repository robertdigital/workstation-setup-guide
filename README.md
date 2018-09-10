![NVIDIA](images/nvidia.png) ![developer](images/developer.png)

# Workstation Setup Guide
Setup guide for the ultimate Deep Learning workstation, powered by NVIDIA

[Tool Guide](nvidia-tools.md) | [Sharing Guide](sharing.md) | [Kubernetes/Kubeflow Guide](kubeflow-setup.md)

### Outline
1. Installing CUDA 9.2
2. Installing cuDNN 7.1
3. Building TensorFlow from source (optional)
4. Installing `nvidia-docker`
5. Using containers from NVIDIA GPU Cloud (NGC)

**This guide is tested on Ubuntu 16.04.**

## Installing NVIDIA drivers + CUDA 9.2

**Preparing the Ubuntu environment**

1. Open the Terminal (`ctrl + alt + T`)
2. Update Ubuntu by running `sudo apt update && sudo apt upgrade -y`
3. Install the SSH server by running `sudo apt install openssh-server -y`
4. Start the SSH service by running `sudo service ssh start`

SSH allows you remote access to your workstation via the command line. This is extremely useful. You may now SSH into your workstation by running `ssh username@ip-address` from a macOS or Linux terminal. If you are using Windows, you will require an SSH client such as [PuTTY](https://www.putty.org/).

**Installing the NVIDIA drivers**

The driver bundled with the CUDA toolkit will work perfectly until the next Ubuntu kernel update is performed, after which the driver may not functional properly. To ensure the driver remains functional across kernel updates, please install the NVIDIA driver the following way:

```
TODO
disable nouveau
```

```
sudo add-apt-repository ppa:graphics-drivers/ppa
sudo apt update
sudo apt install nvidia-396 -y && sudo reboot
```

A system reboot is recommended at this stage.

**Installing the CUDA toolkit**
1. Download the CUDA package (`runfile`) from NVIDIA's [developer site](https://developer.nvidia.com/cuda-downloads?target_os=Linux)
2. Download the cuDNN package from NVIDIA [here](https://developer.nvidia.com/cudnn). You will require a free developer account to download this package.
   **Download the `tar.gz` file**
3. Make sure that you can access these files on your workstation before proceeding.
4. Navigate to the directory in which you stored the CUDA installer
5. Open a command line at your current directory. On most desktop enviroments, you can right click and select "Open Terminal". 
5. `sudo chmod +x *.run*` to make the installers executable
6. Run the installer using `sudo ./<filename>.run`
7. Follow the instructions and agree to everything **except to install the NVIDIA drivers**
   **REPEAT: DO NOT INSTALL THE NVIDIA DRIVERS**

After everything is done, reboot. If your display is not funky, then the NVIDIA drivers have been properly installed. To check the status of your GPUs, run `nvidia-smi` in the Terminal.

## Installing cuDNN 7.1

1. Navigate to the directory in which you downloaded the cuDNN file archive.
2. Extract the files into a folder (`cuda` by default)
3. Copy the files to the correct directories:
	- `sudo cp cuda/include/*.* /usr/local/cuda/include/`
	- `sudo cp cuda/lib64/*.* /usr/local/cuda/lib64/`
4. `sudo nano /etc/ld.so.conf` and add in the following lines:

```
/usr/local/cuda-9.2/lib64
/usr/local/cuda-9.2/lib
```

5. Run `sudo ldconfig`

cuDNN is now installed and working.

## Building TensorFlow from source (optional)

Building TensorFlow from sources ensures that the binary you are using has been compiled with all the optimisations for your target platform. This can squeeze out a little more performance, depending on your system hardware. However, this might take up to a couple of hours. 

**Optional Prerequisites**

1. Update python base packages by running `sudo pip3 install pip setuptools wheel --upgrade`
2. Install the base Python data science stack by running `sudo pip3 install numpy scipy pandas sklearn matplotlib jupyter tensorflow`
   We will install TensorFlow just to ensure that all other dependencies are met. We will replace this TensorFlow with one that we compile ourselves.

**Required Prerequisites**

1. CUDA and cuDNN to be installed and functional.
2. Install TensorFlow from pip to make sure all dependencies are met

For the current version of TensorFlow, you will also need to manually install NCCL.

`TODO: NCCL install guide`

The full instructions can be found on the [TensorFlow webpage](https://www.tensorflow.org/install/install_sources).

## Installing `nvidia-docker`

`nvidia-docker` allows you to run containers that can take full advantage of GPU compute to accelerate tasks. It requires CUDA to be installed on the host machine.

1. Follow [this guide](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-16-04) to install `docker`
2. Follow the [instruction](https://github.com/nvidia/nvidia-docker/wiki/Installation-(version-2.0)) to install `nvidia-docker`

## Using containers from NVIDIA GPU Cloud (NGC)

```
TODO

rough steps:

register for account
configure authentication for registry
pull container
run sample
```
