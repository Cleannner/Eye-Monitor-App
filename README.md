# Eye Monitor App

**项目简介：**

Eye Monitor App 是一个基于 Python 和 OpenCV 的应用程序，用于监测用户的眼睛活动并在检测到闭眼超过一定时间时触发警报。该应用程序利用 Dlib 库进行面部检测和关键点标志预测，通过计算眼睛的纵横比来判断用户是否处于闭眼状态。

**项目组成：**

1. **主要文件：**
   - `eye_monitor.py`: 包含应用程序的主要逻辑，实现了眼睛监测的功能。
   - `alarm.wav`: 警报声音文件。

2. **依赖库：**
   - `cv2`: OpenCV 库，用于图像处理和视频流处理。
   - `dlib`: 用于面部检测和关键点标志预测。
   - `imutils`: 提供一些图像处理的实用功能。
   - `playsound`: 用于播放警报声音。
   - `tkinter`: 用于构建 GUI 窗口。

**使用方法：**

1. 运行 `eye_monitor.py` 文件。
2. 在 GUI 窗口中点击 "开始监测" 按钮，程序将启动摄像头并开始监测眼睛状态。
3. 当检测到用户闭眼连续帧数达到预定阈值时，将触发警报声音和在视频中显示警告文本。
4. 点击 "停止监测" 按钮可停止监测，并点击 "退出" 按钮关闭应用程序。

**注意事项：**

- 在运行应用程序之前，请确保安装了所有依赖库，可以使用以下命令安装：

```bash
pip install opencv-python dlib imutils playsound
```

- 为了正确运行面部检测，确保 `shape_predictor_68_face_landmarks.dat` 文件存在于应用程序目录中。可以在 [Dlib 的官方网站](http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2) 下载该文件。

- 警报声音文件 `alarm.wav` 可以替换为其他音频文件，确保文件路径正确。

**作者：**

该项目由 @Cleannner 创建，可在 [GitHub 仓库链接] 中找到源代码和更多详细信息。

[GitHub 仓库链接]: <https://github.com/Cleannner/Eye-Monitor-App>
