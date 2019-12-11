import datetime
import os

import face_recognition
import time
import cv2

class face_test:
    "Python 人脸测试"


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
def loading(imgFilePaths):
    # 编码库
    sta_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
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
    except FileNotFoundError:
        print("文件不存在")
        return
    image_to_test_encoding = face_recognition.face_encodings(image_to_test)[0]
    # 对比库 相差度
    face_distances = face_recognition.face_distance(li_known_encodings, image_to_test_encoding)
    print("resylts:", face_distances)
    for i, face_distance in enumerate(face_distances):
        result = face_distance < tolerance
        print("对比第{}条。相差度：{}".format(i, face_distance))
        print("-正常截止值为0.3。结果：{}".format(result))
        if result:
            print("识别成功--:{}".format(li_info[i]))
            break
        print()
    end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    print("耗时：", time_sleep(sta_time, end_time))


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
