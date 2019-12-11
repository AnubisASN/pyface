import datetime
import os
import threading

import face_recognition
import time
import cv2


def time_sleep(sta_time, end_time):
    t1 = datetime.datetime.strptime(sta_time, "%Y-%m-%d %H:%M:%S.%f")
    t2 = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S.%f")
    return t2 - t1


def faceCheck():
    print("检测开始时间：", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    img = face_recognition.load_image_file("/super/WorkSpace/PycharmProjects/aobama.png")
    face_locations = face_recognition.face_locations(img)
    print(face_locations)
    print("检测结束时间：", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))


li_info = []
li_known_encodings = []


# 加载识别库
def faceLoading(imgFilePaths):
    # 编码库
    sta_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    li_known_encodings.clear()
    li_info.clear()
    for i, file in enumerate(os.listdir(imgFilePaths)):
        try:
            print("人脸数据加载：#{}:".format(i), imgFilePaths + file)
            image = face_recognition.load_image_file(imgFilePaths + file)
            li_known_encodings.append(face_recognition.face_encodings(image)[0])
            li_info.append(file)
        except Exception:
            print("{}:".format(i), imgFilePaths + file, "发生错误")
    end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    print("识别库加载完成，耗时：", time_sleep(sta_time, end_time))


# 对比识别库
def faceContrast(newImagPath, tolerance):
    sta_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    # 加载是识别人编码
    try:
        image_to_test = face_recognition.load_image_file(newImagPath)
        image_to_test_encoding = face_recognition.face_encodings(image_to_test)[0]
    except FileNotFoundError:
        print("文件不存在")
        return
    # 对比库 相差度
    face_distances = face_recognition.face_distance(li_known_encodings, image_to_test_encoding)
    print("resylts:", face_distances)
    for i, face_distance in enumerate(face_distances):
        result = face_distance < tolerance
        print("对比第{}条。相差度：{}".format(i, face_distance))
        print("-正常截止值为0.3。结果：{}".format(result))
        if result:
            print("识别成功--:{}".format(li_info[i]))
            return li_info[i]
        print()
    end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    print("耗时：", time_sleep(sta_time, end_time))
    return time_sleep(sta_time, end_time)


# 单张对比
def faceContrast0(known_image_path, unknown_image_path, tolerance):
    known_image = face_recognition.load_image_file(known_image_path)
    unknown_image = face_recognition.load_image_file(unknown_image_path)
    known_encoding = face_recognition.face_encodings(known_image)[0]
    unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
    results = face_recognition.compare_faces([known_encoding], unknown_encoding, tolerance)
    face_distances = face_recognition.face_distance([known_encoding], unknown_encoding)
    print("相差度:{}-识别结果：{}".format(face_distances[0], results[0]))


# 循环对比
def faceFor():
    imgName = input("请输入文件名：")
    faceContrast("/home/anubis/Picture/公司人脸名单/" + imgName, 0.35)
    faceFor()


# 库对比
# loading("/home/anubis/Picture/公司人脸名单/")
# print("---------------分割线----------------")
# faceContrast("/super/WorkSpace/PycharmProjects/c.png", 0.35)

# 单张对比
# faceContrast0("/super/WorkSpace/PycharmProjects/test.png", "/super/WorkSpace/PycharmProjects/test.png",0.45)

# 加载库对比
# loading("/home/anubis/Picture/公司人脸名单/")
# faceFor()


# sta_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
# i = 1
# while i < 100:
#     i += 1
# end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
# print(time_sleep(sta_time, end_time))
class thread_loading(threading.Thread):

    def __init__(self, imgFilePaths):
        threading.Thread.__init__(self)
        self.imgFilePaths = imgFilePaths

    def run(self):
        print("加载线程启动")
        faceLoading(self.imgFilePaths)
        print("加载完成，关闭线程")


con_status = 0


class thread_contrast(threading.Thread):

    def __init__(self, imgFilePaths, tolerance):
        threading.Thread.__init__(self)
        self.imgFilePaths = imgFilePaths
        self.tolerance = tolerance

    def run(self):
        if con_status != 1:
            con_status=1

            print("识别线程线程启动")
            faceContrast(self.imgFilePaths, self.tolerance)
            print("加载完成，关闭线程")

    con_status = 0


class thread_test(threading.Thread):

    def __init__(self, tolerance):
        threading.Thread.__init__(self)
        self.tolerance = tolerance

    def run(self):
        print("测试线程线程启动")
        i = 1
        while i < self.tolerance:
            print("测试线程运行")
        print("测试完成，关闭线程")
        time_sleep(0, 500)
