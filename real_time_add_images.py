# 程序目标：读取文件夹中的图片，将图片按照给定的个数添加到另一个文件夹中，并且可以控制线程数，默认为单线程，最后所有影像添加完后生成一个空文件，空文件名为end。
# 程序输入：需要添加的图片所在的文件夹，添加到的文件夹，添加的个数，线程数
# 程序输出：添加完图片后生成一个空文件，空文件名为end
# pip install ThreadPoolExecutorPlus -i https://pypi.tuna.tsinghua.edu.cn/simple
# pip install shutilwhich -i https://pypi.tuna.tsinghua.edu.cn/simple

# 使用：
# python copy_images.py --src_dir E:\PIE-UAV\Data_for_SoftWare\EB\images --dst_dir E:\PIE-UAV\Data_for_SoftWare\EB\newimages --n 10 --t 2000 --threads 4

import os
import argparse
import shutil
from concurrent.futures import ThreadPoolExecutor
import time
import xml.etree.ElementTree as ET
import piexif
from PIL import Image
from PyQt5.QtCore import pyqtSignal, QObject

from tools.kml import read_kml, is_in_poly  # 导入read_kml和is_in_poly函数
from tools.read_exif import ImgExif # 导入类

class SignalHolder(QObject):
    progress_signal = pyqtSignal(int)

signal_holder = SignalHolder()

def copy_img(src_dir, dst_dir, kml_zone, use_kml, img, img_exif):
    orig_path = os.path.join(src_dir, img)

    print(orig_path)
    
    try:
        img_exif.read_gps(orig_path)
    except:
        print("gps error:", orig_path)
        return 
    
    if use_kml:
        is_in = is_in_poly([img_exif.longitude, img_exif.latitude], kml_zone)
        if is_in:
            shutil.copy2(orig_path, os.path.join(dst_dir, img))
    else:
        shutil.copy2(orig_path, os.path.join(dst_dir, img))


def real_time_main(src_dir, dst_dir, kml_path, use_kml, n, t, threads, end, progress):
    if use_kml:
        kml_zone = read_kml(kml_path)
    else:
        kml_zone = ''

    img_files = [file for file in os.listdir(src_dir) if file.endswith(('.JPG', '.jpg', '.jpeg', '.png', '.tif', '.TIF', '.gif'))]
    total = len(img_files)
    progress_count = 0  # 添加一个变量来跟踪已处理的图片数量

    # 设置进度条的最大值为图片的总数
    progress.setMaximum(total)

    img_exif = ImgExif()  # 在主线程中创建 ImgExif 实例

    with ThreadPoolExecutor(max_workers=threads) as executor:
        for i in range(0, len(img_files), n):
            batch = img_files[i:i+n]
            for img in batch:
                executor.submit(copy_img, src_dir, dst_dir, kml_zone, use_kml, img, img_exif)
                progress_count += 1
            time.sleep(t/1000)

            print(progress_count)
            # 发送进度信号
            signal_holder.progress_signal.emit(progress_count)

    executor.shutdown()

    # 创建空文件 'end'
    if end:
        open(os.path.join(dst_dir, 'end'), 'a').close()

    print("实时拷贝影像结束")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--src_dir', type=str, default="E:\\PIE-UAV\\Data_for_SoftWare\\EB\\EB", required=False, help='源图片文件夹')
    parser.add_argument('--dst_dir', type=str, default="E:\\PIE-UAV\\昆明BD联勤保障培训与展示会\\模拟实时写入影像程序\\python\\copy_output_images", required=False, help='目标图片文件夹')
    parser.add_argument('--kml_path', type=str, default="E:\\PIE-UAV\\昆明BD联勤保障培训与展示会\\模拟实时写入影像程序\\python\\kml\\zone.kml", required=False, help="kml区域范围文件全路径")
    parser.add_argument('--use_kml', type=bool, default=False, required=False, help='是否使用kml，默认False')
    parser.add_argument('--n', type=int, default= 1, required=False, help='需要同时复制的图片数量，默认1')
    parser.add_argument('--t', type=int, default= 2000, required=False, help='时间间隔，默认2000毫秒')
    parser.add_argument('--threads', type=int, default=1, required=False, help='线程数，默认1线程')
    parser.add_argument('--end', type=bool, default=False, required=False, help='是否写入end空文件，默认False')

    args = parser.parse_args()

    real_time_main(args.src_dir, args.dst_dir, args.kml_path, args.use_kml, args.n, args.t, args.threads, args.end)