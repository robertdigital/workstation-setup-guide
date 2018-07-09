![NVIDIA](images/nvidia.png) ![developer](images/developer.png)

# Workstation Setup Guide
Setup guide for the ultimate Deep Learning workstation, powered by NVIDIA

To check out some useful tools, see our [tool guide](nvidia-tools.md).

### Outline
1. Installing CUDA 9.2
2. Installing cuDNN 7.1
3. Building TensorFlow from source
4. Installing `nvidia-docker`
5. Configuring remote access (local network)
6. Configuring remote access (via Internet)


## Installing CUDA 9.2

**Preparing the Ubuntu environment**

1. Open the Terminal (`ctrl + alt + T`)
2. Update Ubuntu by running `sudo apt update && sudo apt upgrade -y`
3. Install the SSH server by running `sudo apt install openssh-server -y`
4. Start the SSH service by running `sudo service ssh start`

You may now SSH into your device by running `ssh username@ip-address` from a macOS or Linux terminal. If you are using Windows, you will require an SSH client such as [PuTTY](https://www.putty.org/).

A system reboot is recommended at this stage.

**Preparation steps**
1. Download the CUDA package (`runfile`) from NVIDIA's [developer site](https://developer.nvidia.com/cuda-downloads?target_os=Linux)
2. Download the cuDNN package from NVIDIA [here](https://developer.nvidia.com/cudnn). You will require a free developer account to download this package.
3. Make sure that you can access these files on your workstation before proceeding.

For this section, it is **strongly suggested** that you SSH into your workstation from another device. You will require (minimally) this guide on a seperate device this as you **will** lose access to the graphical user interface (GUI) during this installation process. 

1. Install general package dependencies by running:
	- `sudo apt install build-essential cmake git unzip pkg-config libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libgtk-3-dev libhdf5-serial-dev graphviz libopenblas-dev libatlas-base-dev gfortran -y`
	- `sudo apt install python-dev python-pip python-tk python3-dev python3-pip python3-tk python-imaging-tk -y`
2. Install generic linux headers (required to switch to NVIDIA drivers):
	- `sudo apt install linux-image-generic linux-image-extra-virtual linux-source linux-headers-generic`
3. Stop the X server (GUI) by running `sudo service lightdm stop`
4. We will now disable the open-source Nouveau graphics driver: `sudo nano /etc/modprobe.d/blacklist-nouveau.conf`
5. Add the following lines to the file (`ctrl + shift + V` or `CMD + V` to paste):

```
blacklist nouveau
blacklist lbm-nouveau
options nouveau modeset=0
alias nouveau off
alias lbm-nouveau off
```

6. Press `ctrl + X` to save the file and exit the `nano` text editor.
7. `echo options nouveau modeset=0 | sudo tee -a /etc/modprobe.d/nouveau-kms.conf`
8. `sudo update-initramfs -u`
9. `sudo reboot`

Wait for your workstation to reboot, then SSH in again. If your display looks funky, you're doing it right. Once again, run `sudo service lightdm stop` to disable the X server before proceeding.

10. Navigate to the directory in which you stored the CUDA installer using the `cd` command
11. `sudo chmod +x *.run*` to make the installer executable
12. Run the installer using `sudo ./<filename>.run`
13. Follow the instructions and agree to everything

After everything is done, reboot. If your display is no longer funky, then the NVIDIA drivers have been properly installed. To check the status of your GPUs, run `nvidia-smi` in the Terminal.

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

## Building TensorFlow from source

**Optional Prerequisites**

1. Update python base packages by running `sudo pip3 install pip setuptools wheel --upgrade`
2. Install the entire Python data science stack by running `sudo pip3 install numpy scipy pandas sklearn matplotlib jupyter opencv-contrib-python tensorflow`

**Required Prerequisites**

1. CUDA and cuDNN to be installed and functional.
2. Install TensorFlow from pip to make sure all dependencies are met

The full instructions can be found on the [TensorFlow webpage](https://www.tensorflow.org/install/install_sources).

## Installing `nvidia-docker`

`nvidia-docker` allows you to run containers that can take full advantage of GPU compute to accelerate tasks. It requires CUDA to be installed on the host machine.

1. Follow [this guide](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-16-04) to install `docker`
2. Follow the [instruction](https://github.com/nvidia/nvidia-docker/wiki/Installation-(version-2.0)) to install `nvidia-docker`

## Configuring remote desktop access (local network)

### 1. Setup

Remote command line access is provided by SSH (previously configured)

We will install a lightweight desktop enviroment (XFCE) and a VNC server to provide remote desktop capabilities.

`sudo apt install xfce4 xfce4-goodies tightvncserver`

Use the command `vncserver` to start the remote desktop service under your current user:

```
$ vncserver

New 'X' desktop is your-workstation:1

Starting applications specified in /home/nvaitc/.vnc/xstartup
Log file is /home/nvaitc/.vnc/your-workstation:1.log
```

On initial startup, you will be prompted to set a password for your user. Individual accounts on the workstation can each start individual remote desktops to be used simultaneously.

Use `vncserver -kill :1` to kill Desktop `:1`

After initial setup, kill the VNC server and replace the contents of the `xstartup` file:

`nano ~/.vnc/xstartup`

```
#!/bin/sh

xrdb $HOME/.Xresources
xsetroot -solid grey
#x-terminal-emulator -geometry 80x24+10+10 -ls -title "$VNCDESKTOP Desktop" &
#x-window-manager &
# Fix to make GNOME work
startxfce4 &
export XKL_XMODMAP_DISABLE=1
/etc/X11/Xsession
```

### 2. Connecting

On your client device (phone/tablet/laptop) download a VNC Client. [RealVNC Viewer](https://www.realvnc.com/en/connect/download/viewer/) works on all common platforms without an issue.

Connect by entering the ip-address of your workstation and the desktop number as follows:

![VNC_Connect](images/vnc_viewer.png)

Dismiss any security warning and enter in your password. You will then be presented with your remote desktop:

![VNC_Desktop](images/vnc_desktop.png)

You can use the remote desktop to run Jupyter Notebook sessions in a persistent manner as the state of the desktop and applications will persist between connections.

## Configuring remote access (via Internet)

`TODO`

Mainly SSH reverse tunneling and RealVNC Home.

Somewhere along the way there's a need to edit the `/etc/ssh/sshd_config` file.

