# ProVision - Weather Effect Removal from Images  
### Enhancing Image Quality Using Image Processing & Deep Learning  

## Project Overview  
Weather conditions such as rain, fog, haze, and snow degrade image quality, impacting various real-world applications like autonomous driving, surveillance systems, and satellite imaging. This project presents a hybrid approach that integrates traditional image processing and deep learning techniques to remove weather effects and restore image clarity.  

## Key Features  
- **Haze Removal**: Implemented using **Dark Channel Prior (DCP)** method.  
- **Rain Streak & Drop Removal**: Uses U-Net with Attention Mechanism & MPRNet for effective restoration.  
- **Snow Removal**: CNN-based techniques for noise reduction.  
- **Performance Evaluation**: Assessed using PSNR, SSIM, MSE Hybrid Loss, and contrast improvement metrics.  
- **Dataset Handling**: Collected from **Kaggle, GitHub repositories, and Google Images** with preprocessing steps for improved results.  

## Tech Stack  
- **Programming Language**: Python  
- **Deep Learning Frameworks**: TensorFlow, Keras, PyTorch  
- **Image Processing**: OpenCV, NumPy  
- **Models Used**:  
  - U-Net with Attention Mechanism  
  - RIDNet (Deep Learning for Single-Image Deraining)  
  - MPRNet (Multi-Stage Processing for Rain Removal)    

