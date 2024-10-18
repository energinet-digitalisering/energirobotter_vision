# Energirobotter Elrik

Packages for the Elrik Humanoid Robot, part of the project "Energirobotter". 

## Setup

Clone this repository into a `workspace/src/` folder, along with [zed-ros2-wrapper](https://github.com/stereolabs/zed-ros2-wrapper) (run commands from root of `workspace`):

```
git clone git@github.com:energinet-digitalisering/energirobotter-elrik.git src/energirobotter-elrik/
git clone  --recursive https://github.com/stereolabs/zed-ros2-wrapper.git
```

Download and install [CUDA 12.6](https://developer.nvidia.com/cuda-downloads).

Download and install [ZED SDK v4.1](https://www.stereolabs.com/en-dk/developers/release) for CUDA 12. When prompted if the ZED SDK installer shall install CUDA, say no. 


### Dependencies

In `worspace` root, source ROS and install ROS dependencies with rosdep:
```
source /opt/ros/humble/setup.bash
rosdep install --from-paths src --ignore-src -r -y
```

Python modules not included in [rosdistro](https://github.com/ros/rosdistro/blob/master/rosdep/python.yaml) can be installed from root of workspace with:
```
pip install -r src/energirobotter-elrik/requirements.txt
```

### AI model
Download face detection model [yolov8n-face.pt](https://github.com/akanametov/yolov8-face/releases/download/v0.0.0/yolov8n-face.pt) from the [yolo-face repository](https://github.com/akanametov/yolo-face/tree/v0.0.0). Move the model into the `src/energirobotter-elrik/face_detection/models/` directory.


### Build

Build `workspace` with:
```
colcon build --symlink-install
```

## Usage

Use the `elrik_bringup` package's `vision.launch.py` to start the camera and face detection:

```
source install/setup.bash
ros2 launch elrik_bringup vision.launch.py use_compressed:=true
```

If no camera is available, run example with:
```
ros2 launch elrik_bringup vision.launch.py use_mock_camera:=true
```

> Note: The first time `face_detection` is run `ultralytics` will install som extra packages, and require a restart of the node.

