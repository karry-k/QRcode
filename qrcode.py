# coding: utf8

import pyqrcode
import shortuuid
import zbarlight
from PIL import Image
import cv2
import pyzbar.pyzbar as pyzbar
import time
import sys
from pyzbar.pyzbar import decode

type_image = ['.jpg', '.JPG','.jpeg', '.JPEG', '.JPE', '.png',  '.bmp', '.gif', '.tiff']


def qr_code(url):
    url_ob = pyqrcode.create(url)
    image = url_ob.png("" + shortuuid.uuid(name=url) + ".png", scale=7)
    return image


def to_diff_type(name_jpg):
    for x in type_image:
        try:
            im = Image.open(""+name_jpg+".png")
            name_image = im.save(""+name_jpg+x)
        except:
            pass


def qr_decode(name_image):
    for x in type_image:
        try:
            with open("" + name_image + x, 'rb') as image_file:
                image = Image.open(image_file)
                image.load()
                codes = zbarlight.scan_codes("qrcode", image)
                if codes is None:
                    photo_to_graybin(name_image)
                    try:
                        with open("" + name_image + x, 'rb') as image_file:
                            image = Image.open(image_file)
                            image.load()
                            codes = zbarlight.scan_codes("qrcode", image)
                            count_codes = len(codes)
                            for i in range(count_codes):
                                print(i, "QR decoded: %s" % codes[i].decode("utf-8"))
                            return codes
                            if codes is None:
                                print("Не удалось распознать QR код.")
                                return "Не удалось распознать QR код."
                                break
                    except:
                        pass
                    break
                count_codes = len(codes)
                for i in range(count_codes):
                    print(i, "QR decoded: %s" % codes[i].decode("utf-8"))
                return codes
        except FileNotFoundError:
            pass


def photo_to_graybin(name_photo):
    im_gray = cv2.imread("" + name_photo + ".jpg", cv2.IMREAD_GRAYSCALE)
    (thresh, im_bw) = cv2.threshold(im_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    im_bw = cv2.threshold(im_gray, thresh, 255, cv2.THRESH_BINARY)[1]
    cv2.imwrite("" + name_photo + ".jpg", im_bw)


def read_qr_code(frame):
    qr_on_frame = pyzbar.decode(frame)
    for qr in qr_on_frame:
        print(qr.data)
        return qr.data


def get_video():
    cap = cv2.VideoCapture(0)
    while (cap.isOpened()):
        _, frame = cap.read()
        cv2.imshow("qrcode", frame)
        if read_qr_code(frame):
            print(read_qr_code(frame))
            break
        if cv2.waitKey(30) == ord("q"):
            sys.exit()
    cap.release()
    cv2.imwrite('messigray.png', frame)
    time.sleep(2)
    cv2.destroyAllWindows()



def decode_and_draw(name_photo):
    text = qr_decode(name_photo)
    coordinates = decode(Image.open("" + name_photo + ".jpg"))
    n_obj = len(coordinates)
    x = []
    y = []

    for i in range(n_obj):
        for j in range(4):
            x.append(coordinates[i][3][j][0])
            y.append(coordinates[i][3][j][1])

    image = cv2.imread("" + name_photo + ".jpg")
    lineThickness = 2
    lines = []
    # рисуем границы для декодированных QR кодов и выводим на фотографию текст(url)
    j = 0
    for i in range(n_obj * 4):
        if i == 0:
            lines.append(cv2.line(image, (x[i], y[i]), (x[i + 1], y[i + 1]), (0, 255, 0), lineThickness))
        elif (i + 1) % 4 == 0:
            j += 1
            lines.append(cv2.line(image, (x[i], y[i]), (x[i - 3], y[i - 3]), (0, 255, 0), lineThickness))
            cv2.putText(image, text[i - 3 * j].decode("utf-8"), (x[i], y[i]), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                        (193, 0, 32), 2)
        else:
            lines.append(cv2.line(image, (x[i], y[i]), (x[i + 1], y[i + 1]), (0, 255, 0), lineThickness))

    for i in range(len(lines)):
        cv2.imwrite("" + name_photo + ".jpg", lines[i])


name_photo = "../QRcode/img/name"
# qr_decode(name_photo)
decode_and_draw(name_photo)
# photo_to_graybin(name_photo)
# qr_code("https://www.google.com.ua/")
# to_diff_type(name_photo)
# get_video()
# read_qr_code(name_photo)
