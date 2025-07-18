# Smart Fan Control Using Image Processing

> **Your Comfort, Your Gesture** - Control your fan with simple hand gestures using computer vision and machine learning.

## 🌟 Overview

This project demonstrates an innovative approach to fan control using hand gesture recognition. By leveraging OpenCV, TensorFlow, and ESP32 microcontrollers, users can control fan functions through intuitive hand gestures captured by an ESP32-CAM module.

## ✨ Features

- **Gesture-Based Control**: Control fan with 5 different hand gestures
- **Real-Time Processing**: Instant gesture recognition and response
- **Wireless Operation**: Wi-Fi enabled ESP32 modules for remote control
- **Visual Feedback**: LED indicators for current fan status
- **Multiple Speed Levels**: Variable fan speed control (0-3 levels)
- **User-Friendly Interface**: Intuitive gesture mapping for all ages

## 🎯 Supported Gestures

| Gesture | Function | Description |
|---------|----------|-------------|
| ✊ Rock | Fan OFF | Turns off the fan completely |
| 👍 Thumbs Up | Fan ON | Turns on fan at level 1 |
| ✋ Paper | Max Speed | Sets fan to maximum speed (level 3) |
| ✌️ Scissors | Speed Down | Decreases fan speed by one level |
| ☝️ Up | Speed Up | Increases fan speed by one level |

## 🛠️ Hardware Requirements

### ESP32-CAM Module
- ESP32-CAM board
- Camera module (OV2640)
- Wi-Fi connectivity
- Power supply (5V)

### ESP32 Controller
- ESP32 development board
- Fan motor
- LED indicators
- Relay modules for fan control
- Power supply

## 💻 Software Requirements

### Python Environment
- Python 3.8+
- OpenCV (`cv2`)
- TensorFlow
- NumPy
- Requests
- CVZone
- PIL (Pillow)

### Arduino IDE
- ESP32 board package
- Required libraries:
  - `esp_camera.h`
  - `WiFi.h`
  - `esp_http_server.h`

## 📦 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/K-B-R-S-W/smart-fan-control.git
cd smart-fan-control
```

### 2. Python Dependencies
```bash
pip install opencv-python tensorflow numpy requests cvzone pillow
```

### 3. Arduino Setup
1. Install ESP32 board package in Arduino IDE
2. Install required libraries through Library Manager
3. Upload `esp32cam.ino` to your ESP32-CAM module

## 🚀 Quick Start

### 1. Hardware Setup
1. Connect ESP32-CAM according to the pin configuration in `esp32cam.ino`
2. Set up ESP32 controller with fan and LED connections
3. Power on both modules

### 2. Network Configuration
Update Wi-Fi credentials in the Arduino code:
```cpp
const char* ssid = "Your_WiFi_SSID";
const char* password = "Your_WiFi_Password";
```

### 3. IP Address Configuration
Update the IP addresses in Python scripts:
```python
ESP32_IP_cam = "http://('Your IP')" 
ESP32_IP = "http://('Your IP')"    
```

### 4. Model Setup
1. Place your trained `keras_model.h5` in the project directory
2. Ensure `labels.txt` contains the correct gesture labels
3. Update file paths in the Python scripts

### 5. Run the Application
```bash
# For local webcam
python mainwithcam.py

# For ESP32-CAM stream
python main.py
```

## 📁 Project Structure

```
smart-fan-control/
├── esp32cam.ino       
├── main.py              
├── mainwithcam.py       
├── labels.txt            
├── keras_model.h5        
├── .python-version      
├── README.md             
└── docs/
    └── Smart Fan Control Using Image Processing.pdf
```

## 🔧 Configuration

### ESP32-CAM Pin Configuration
```cpp
#define PWDN_GPIO_NUM     32
#define RESET_GPIO_NUM    -1
#define XCLK_GPIO_NUM      0
#define SIOD_GPIO_NUM     26
#define SIOC_GPIO_NUM     27
#define Y9_GPIO_NUM       35
#define Y8_GPIO_NUM       34
#define Y7_GPIO_NUM       39
#define Y6_GPIO_NUM       36
#define Y5_GPIO_NUM       21
#define Y4_GPIO_NUM       19
#define Y3_GPIO_NUM       18
#define Y2_GPIO_NUM        5
#define VSYNC_GPIO_NUM    25
#define HREF_GPIO_NUM     23
#define PCLK_GPIO_NUM     22
```

### HTTP API Endpoints
- `GET /fanon` - Turn fan on (level 1)
- `GET /fanoff` - Turn fan off
- `GET /fanspeedup` - Increase fan speed
- `GET /fanspeeddown` - Decrease fan speed
- `GET /fanlevel3` - Set fan to maximum speed

## 🧠 Machine Learning Model

### Training Details
- **Dataset**: 25,000 images (5,000 per class)
- **Classes**: 5 gesture types
- **Training Platform**: Teachable Machine
- **Parameters**:
  - Epochs: 50
  - Batch Size: 16
  - Learning Rate: 0.001

### Model Architecture
- Input Size: 224x224x3 (RGB images)
- Output: 5 classes (gesture types)
- Format: TensorFlow Keras (.h5)

## 🔍 Troubleshooting

### Common Issues

#### ESP32-CAM Connection Issues
- Check Wi-Fi credentials
- Verify IP address assignment
- Ensure proper power supply (5V, adequate current)

#### Gesture Recognition Problems
- Ensure proper lighting conditions
- Keep hand within camera frame
- Maintain consistent hand positioning
- Check model file path and format

#### Performance Issues
- Verify GPU configuration for TensorFlow
- Check network latency between devices
- Ensure adequate processing power

### Debug Mode
Enable debug output in Python:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📊 Performance Metrics

- **Gesture Recognition Accuracy**: >95%
- **Response Time**: <100ms
- **Frame Rate**: 30 FPS
- **Detection Range**: 0.5-2 meters
- **Power Consumption**: <2W (ESP32 modules)

## 🛡️ Safety Features

- **Connection Monitoring**: Automatic reconnection on network issues
- **Error Handling**: Graceful handling of hardware failures
- **Timeout Protection**: Prevents system hang-ups
- **Safe Shutdown**: Proper cleanup on exit

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 🙏 Acknowledgments

- OpenCV community for computer vision tools
- TensorFlow team for machine learning framework
- ESP32 community for hardware support
- CVZone for hand tracking utilities

## 📞 Support

For support, please open an issue in the GitHub repository or contact the development team.
