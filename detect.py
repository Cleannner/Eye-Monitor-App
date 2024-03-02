import cv2
import dlib
import imutils
import playsound
from imutils import face_utils
from imutils.video import VideoStream
from scipy.spatial import distance as dist
import tkinter as tk
from tkinter import ttk
from threading import Thread

# 摄像头索引、面部标志检测器模型路径和警告声音文件路径
WEBCAM_INDEX = 0
SHAPE_PREDICTOR_PATH = 'shape_predictor_68_face_landmarks.dat'
ALARM_PATH = 'alarm.wav'

# 眼睛纵横比阈值和连续帧数
EYE_AR_THRESH = 0.3
EYE_AR_CONSE_FRAMES = 48

# 初始化计数器和警报标志
COUNTER = 0
ALARM_ON = False


def sound_alarm(path):
    # 播放警告声音
    playsound.playsound(path)


def eye_aspect_ratio(eye):
    # 计算眼睛纵横比
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear


class EyeMonitorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Eye Monitor App")

        self.vs = None  # VideoStream object
        self.monitoring = False  # Flag to indicate whether eye monitoring is active

        (self.lStart, self.lEnd) = face_utils.FACIAL_LANDMARKS_IDXS['left_eye']
        (self.rStart, self.rEnd) = face_utils.FACIAL_LANDMARKS_IDXS['right_eye']

        self.create_widgets()

    def create_widgets(self):
        # 创建 GUI 窗口组件
        self.start_button = ttk.Button(self.master, text="开始监测", command=self.start_monitoring)
        self.start_button.pack(pady=10)

        self.stop_button = ttk.Button(self.master, text="停止监测", command=self.stop_monitoring, state=tk.DISABLED)
        self.stop_button.pack(pady=10)

        self.quit_button = ttk.Button(self.master, text="退出", command=self.quit_app)
        self.quit_button.pack(pady=10)

        # 视频处理线程
        self.video_thread = None

    def start_monitoring(self):
        self.monitoring = True
        self.vs = VideoStream(src=WEBCAM_INDEX, usePiCamera=False).start()

        # 启动视频处理线程
        self.video_thread = Thread(target=self.monitor_eyes)
        self.video_thread.daemon = True
        self.video_thread.start()

        # 更新按钮状态
        self.start_button["state"] = tk.DISABLED
        self.stop_button["state"] = tk.NORMAL

    def stop_monitoring(self):
        self.monitoring = False
        self.vs.stop()
        self.video_thread.join()

        # 更新按钮状态
        self.start_button["state"] = tk.NORMAL
        self.stop_button["state"] = tk.DISABLED

    def quit_app(self):
        self.stop_monitoring()
        self.master.destroy()

    def monitor_eyes(self):
        global COUNTER, ALARM_ON

        while self.monitoring:
            frame = self.vs.read()
            frame = imutils.resize(frame, width=450)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # 在灰度图上检测面部
            rects = detector(gray, 0)

            for rect in rects:
                # 获取面部关键点坐标
                shape = predictor(gray, rect)
                shape = face_utils.shape_to_np(shape)

                # 提取左右眼区域
                left_eye = shape[self.lStart:self.lEnd]
                right_eye = shape[self.rStart:self.rEnd]

                # 计算左右眼的纵横比
                left_ear = eye_aspect_ratio(left_eye)
                right_ear = eye_aspect_ratio(right_eye)

                # 计算平均纵横比
                ear = (left_ear + right_ear) / 2.0

                # 绘制眼睛区域的凸包
                left_eye_hull = cv2.convexHull(left_eye)
                right_eye_hull = cv2.convexHull(right_eye)
                cv2.drawContours(frame, [left_eye_hull], -1, (0, 255, 0), 1)
                cv2.drawContours(frame, [right_eye_hull], -1, (0, 255, 0), 1)

                # 判断眼睛纵横比是否低于阈值
                if ear < EYE_AR_THRESH:
                    COUNTER += 1

                    # 判断是否连续帧数达到阈值，触发警报
                    if COUNTER >= EYE_AR_CONSE_FRAMES and not ALARM_ON:
                        ALARM_ON = True

                        # 播放警报声音（在新线程中以避免阻塞主线程）
                        if ALARM_PATH:
                            t = Thread(target=sound_alarm, args=(ALARM_PATH,))
                            t.daemon = True
                            t.start()

                        # 在视频帧上添加警告文本
                        cv2.putText(frame, '警告！', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                else:
                    # 重置计数器和警报标志
                    COUNTER = 0
                    ALARM_ON = False

                # 在视频帧上添加当前眼睛纵横比的文本显示
                cv2.putText(frame, 'ERA:{:2f}'.format(ear), (300, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

            # 显示视频帧
            cv2.imshow('Frame', frame)
            key = cv2.waitKey(1) & 0xFF

            # 按下 'q' 键停止监测
            if key == ord('q'):
                self.stop_monitoring()

        # 关闭 OpenCV 窗口
        cv2.destroyAllWindows()


def main():
    root = tk.Tk()
    app = EyeMonitorApp(root)
    root.mainloop()


if __name__ == "__main__":
    # 加载 Dlib 面部检测器和关键点标志预测器
    print("[INFO]加载面部标志...")
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(SHAPE_PREDICTOR_PATH)

    main()
