import numpy as np
import cv2
import math
import random
import os

def img_to_gray(image_path , filename):
    img = cv2.imread(image_path)
    gray_img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    gray_img = cv2.resize(gray_img,(512,512),interpolation=cv2.INTER_AREA)
    gray_filepath = os.path.join('static/img','aip_'+ 'gray_' + filename  )
    cv2.imwrite(gray_filepath,gray_img)
    return gray_filepath

def img_to_histogram(image_path , filename):
    img = cv2.imread(image_path)
    hist = cv2.calcHist([img], [0], None, [256], [0, 256])
    hist_img = np.zeros((512, 512, 3), dtype=np.uint8)
    cv2.normalize(hist, hist, 0, 512, cv2.NORM_MINMAX)
    bin_width = 512 // 256  # 每個bin的寬度
    for x, y in enumerate(hist):
        cv2.rectangle(hist_img, (x * bin_width, 512), ((x + 1) * bin_width, 512 - int(y)), (255, 255, 255), -1)
    histogram_filepath = os.path.join('static/img', 'aip_'+ 'histogram_' + filename)
    cv2.imwrite(histogram_filepath, hist_img)
    return histogram_filepath

def img_to_gaussion_noise(image_path, filename):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    gaussion_noise_img = np.copy(img)
    sigma = 50
    for x in range(gaussion_noise_img.shape[0]):
        for y in range(gaussion_noise_img.shape[1]):
            r = random.random()  # step2
            phi = random.random()  # step2
            z1 = sigma * math.cos(2 * math.pi * phi) * (-2 * math.log(r)) ** 0.5  # step3
            
            f1 = gaussion_noise_img[x, y] + z1  # step4
            if f1 < 0:
                gaussion_noise_img[x, y] = 0  # step5
            elif f1 > 255:
                gaussion_noise_img[x, y] = 255  # step5
            else:
                gaussion_noise_img[x, y] = f1  # step5

    gaussion_noise_filepath = os.path.join('static/img', 'aip_' + 'gaussion_noise_' + filename)
    cv2.imwrite(gaussion_noise_filepath, gaussion_noise_img)
    return gaussion_noise_filepath

def img_to_haar_wavelet(image_path, filename):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)  # 確保圖像是灰度圖像
    level = 1
    decompose = 1
    levelused = 1
    rows, cols = img.shape  # 確保行列數與圖像大小一致
    tmp = np.zeros((rows, cols), dtype=np.int64)  # 修改為 int64 以避免溢出
    wav = np.zeros((rows, cols), dtype=np.int64)  # 修改為 int64 以避免溢出

    while decompose <= level:
        width = rows // levelused
        height = cols // levelused
        for i in range(int(width)):
            for j in range(height // 2):
                tmp_val1 = int((img[i, 2 * j] // 2 + img[i, 2 * j + 1]) // 2)
                tmp[i, j] = np.clip(tmp_val1, 0, 255)
                if tmp[i, j] > 255 or tmp[i, j] < 0:
                    print("overflow__", tmp[i, j])

                tmp_val2 = int(np.int64(img[i, 2 * j]) - np.int64(img[i, 2 * j + 1]))
                tmp[i, j + int(height // 2)] = np.clip(tmp_val2, 0, 255)
                if tmp[i, j + int(height // 2)] > 255 or tmp[i, j + int(height // 2)] < 0:
                    print("overflow___", tmp[i, j + int(height // 2)])

        for i in range(int(width // 2)):
            for j in range(int(height)):
                wav_val1 = int(tmp[2 * i, j] + tmp[2 * i + 1, j])
                wav[i, j] = np.clip(wav_val1, 0, 255)
                if wav[i, j] > 255 or wav[i, j] < 0:
                    print("overflow", wav[i, j])

                wav_val2 = int((tmp[2 * i, j] - tmp[2 * i + 1, j]) // 2)
                wav[i + int(width // 2), j] = np.clip(wav_val2, 0, 255)
                if wav[i + int(width // 2), j] > 255 or wav[i + int(width // 2), j] < 0:
                    print("overflow", wav[i + int(width // 2), j])
        img = wav
        decompose += 1
        levelused *= 2

    haar_wavelet_filepath = os.path.join('static/img', 'aip_' + 'haar_wavelet_' + filename)
    cv2.imwrite(haar_wavelet_filepath, img)
    return haar_wavelet_filepath

def img_to_histogram_equalization(image_path, filename):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    for_histogramequalization_img =cv2.resize(img,(512,512),interpolation=cv2.INTER_AREA)
    arrayH=[]
    dictarrayH={}
    arrayHC=[]
    Hmin=0

    #第一用出出現次數
    for i in range(256): #先把字典建出來
        dictarrayH[i]=0
    
    for x in range(512):
        for y in range(512):
            arrayH.append(for_histogramequalization_img[x][y])
    for i in arrayH:
        dictarrayH[i]=dictarrayH[i]+1
    #弄HC
    addall=0
    for i in dictarrayH:
        addall=addall+dictarrayH[i]
        arrayHC.append(addall)
    for i in arrayHC:
        if i != 0:
            Hmin=i
            break
    for x in range(512):
        for y in range(512):
            for_histogramequalization_img[x][y]=round((arrayHC[for_histogramequalization_img[x][y]]-Hmin)/(262144-Hmin)*255)

    histogram_equalization_filepath = os.path.join('static/img', 'aip_' + 'histogram_equalization_' + filename)
    cv2.imwrite(histogram_equalization_filepath, for_histogramequalization_img)
    return histogram_equalization_filepath


