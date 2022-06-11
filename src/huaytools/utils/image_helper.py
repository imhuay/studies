#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time:
    2021-03-09 8:56 PM
    
Author:
    huayang
    
Subject:
    图片完整性检查
"""
import io
import os

try:
    import cv2
except ImportError:
    pass

import numpy as np
import matplotlib.pyplot as plt

from PIL import Image


class ImageCheck:
    """@Image Utils
    图片完整性检查

    Examples:
        >>> img = r'./_test_data/pok.jpg'
        >>> ImageCheck.is_complete(img)

    """

    @staticmethod
    def is_jpg(img_byte):
        """"""
        return img_byte[6:10] in (b'JFIF', b'Exif')

    @staticmethod
    def is_png(img_byte):
        return img_byte.startswith(b'\211PNG\r\n\032\n')

    @staticmethod
    def is_gif(img_byte):
        return img_byte[:6] in (b'GIF87a', b'GIF89a')

    @staticmethod
    def is_bmp(img_byte):
        return img_byte.startswith(b'BM')

    @staticmethod
    def is_complete_jpg(byte_str):
        b = byte_str.rstrip(b'\0\r\n')
        return b.endswith(b'\xff\xd9')

    @staticmethod
    def is_complete_png(byte_str):
        b = byte_str.rstrip(b'\0\r\n')
        return b.endswith(b'\x60\x82\x00') or b.endswith(b'\x60\x82')

    # def is_complete_bmp(byte_str):
    #     size = int(b'0x' + byte_str[2:6][::-1], 16)
    #     return size <= len(byte_str)

    @staticmethod
    def is_complete_img(byte_str):
        """不一定有效，其他类型建议先转换成 jpg 或 png"""
        try:
            from PIL import Image
            Image.open(io.BytesIO(byte_str)).verify()
        except:
            return False
        return True

    @staticmethod
    def is_complete(img):
        """
        判断图片是否完整

        Args:
            img: 图像路径，或二进制字符串，如 open(file, 'rb').read()、requests.get(url).content 等
        """

        if isinstance(img, str):
            with open(img, 'rb') as f:
                img = f.read()

        if ImageCheck.is_jpg(img):
            return ImageCheck.is_complete_jpg(img)
        elif ImageCheck.is_png(img):
            return ImageCheck.is_complete_png(img)
        else:
            return ImageCheck.is_complete_img(img)


def get_real_ext(image_path, return_is_same=False):
    """@Image Utils
    获取图像文件的真实后缀
    如果不是图片，返回后缀为 None
    该方法不能判断图片是否完整

    Args:
        image_path:
        return_is_same: 是否返回 `is_same`

    Returns:
        ext_real, is_same
        真实后缀，真实后缀与当前后缀是否相同
        如果当前文件不是图片，则 ext_real 为 None
    """
    import imghdr

    # 获取当前后缀
    ext_cur = os.path.splitext(image_path)[1]

    if ext_cur.startswith('.'):
        ext_cur = ext_cur[1:]

    # 获取真实后缀
    ext_real = imghdr.what(image_path)

    if return_is_same:
        # 是否相同
        is_same = ext_cur == ext_real or {ext_cur, ext_real} == {'jpg', 'jpeg'}

        return ext_real, is_same

    return ext_real


def rename_to_real_ext(image_path):
    """将图片重命名为真实后缀"""
    ext_real, is_same = get_real_ext(image_path, return_is_same=True)

    if is_same or ext_real is None:
        return

    prefix, _ = os.path.splitext(image_path)
    dst = '.'.join([prefix, ext_real])
    os.rename(image_path, dst)


def load_image(src, color_mode='RGB') -> Image.Image:
    """
    加载原始图像，返回 PIL.Image 对象

    Args:
        src(str or bytes): 图像路径，或二进制数据
        color_mode(str): 颜色模式，支持 {"L","RGB","RGBA"} 种类型，对应的 shape 分别为 (w, h)、(w, h, 3)、(w, h, 4)

    Returns: Image.Image
    """
    if isinstance(src, bytes):
        img = Image.open(io.BytesIO(src))
    else:
        with open(src, 'rb') as f:
            img = Image.open(io.BytesIO(f.read()))

    if color_mode not in {"L", "RGB", "RGBA"}:
        raise ValueError('Unsupported color_mode: %s, it must be one of {"L", "RGB", "RGBA"}' % color_mode)

    if img.mode != color_mode:
        try:
            img = img.convert(color_mode)
        except:
            print('The color mode=%s can not convert to %s' % (img.mode, color_mode))

    return img


def tensor_to_image(x, save_path=None, scale=False):
    """
    将 numpy 数组转为 PIL.Image 对象

    Args:
        x:
        save_path:
        scale:

    """
    x = np.asarray(x, np.float32)

    if scale:
        x = x - np.min(x)
        x_max = np.max(x)
        if x_max != 0:
            x = x / x_max
        x *= 255

    if x.ndim == 3:
        n_channel = x.shape[2]
        if n_channel == 3:
            color_mode = 'RGB'
        elif n_channel == 4:
            color_mode = 'RGBA'
        elif n_channel == 1:
            x = x[:, :, 0]
            color_mode = 'I' if np.max(x) > 255 else 'L'
        else:
            raise ValueError('Unsupported channel number: %s, it must be one of {1, 3, 4}' % n_channel)
    elif x.ndim == 2:
        color_mode = 'I' if np.max(x) > 255 else 'L'
    else:
        raise ValueError('Unsupported tensor dim: %s, it must be one of {2, 3}' % x.ndim)

    dtype = np.int32 if color_mode == 'I' else np.uint8
    img = Image.fromarray(x.astype(dtype), color_mode)

    if save_path:
        img.save(save_path)

    return img


class ImageTensorize(object):
    """
    图片张量化，提供了基于 PIL、cv2、tf 的三种方法；三种方法获取的张量在数值上会存在细微差异

    Note:
        - 基于 base64 的序列化方法可以参考：python_utils/basic_utils/serialize.py
        - 使用 tf 版本需要 tensorflow >= 2.0，因为用到了 x.numpy()
        - cv2 读取的图片默认通道顺序为 bgr，这个需要注意：
            - 如果要把 cv2 读取的图片用其他库处理，则需要先调整为 rgb；反之其他库处理的图片传给 cv2，需要先转回 bgr；
            - 换言之，尽量使用同一套库，要么都用 cv2 处理，要么都不用；

    References:
        keras.preprocessing.image
    """

    @staticmethod
    def by_pil(img, resize=None, color_mode='RGB', dtype=np.uint8):
        """
        将 PIL.Image 对象转为 numpy 数组

        Args:
            img(str or bytes or Image.Image):
            resize:
            color_mode: 只支持 {"L","RGB","RGBA"}，如果是其他更专业的模式，参考 plt.imread、plt.pil_to_array 等的实现
            dtype:

        Returns:

        """
        if isinstance(img, (str, bytes)):
            img = load_image(img, color_mode=color_mode)

        if resize:
            img = img.resize(size=resize)

        x = np.asarray(img, dtype=dtype)
        if len(x.shape) == 2:
            x = x.reshape((x.shape[0], x.shape[1], 1))

        return x

    @staticmethod
    def by_cv2(img, resize=None, color_mode=None, convert_to_rgb=True):
        """
        Args:
            img:
            resize:
            color_mode: 默认 cv2.IMREAD_COLOR
            convert_to_rgb: 是否将通道顺序转为 'RGB'，cv2 默认的通道顺序为 'BGR'

        """
        if color_mode is None:
            color_mode = cv2.IMREAD_COLOR

        if isinstance(img, str):
            with open(img, 'rb') as f:
                img = f.read()

        x = cv2.imdecode(np.frombuffer(img, dtype=np.uint8), flags=color_mode)

        if resize:
            x = cv2.resize(x, dsize=resize)

        if convert_to_rgb:
            x = cv2.cvtColor(x, cv2.COLOR_BGR2RGB)

        return x

    @staticmethod
    def by_tf(img, resize=None, return_numpy=False, expand_animations=False):
        """
        Args:
            img:
            resize:
            return_numpy:
            expand_animations: 默认 False，即 gif 只取第一帧
        """
        import tensorflow as tf

        if isinstance(img, str):
            with open(img, 'rb') as f:
                img = f.read()

        x = tf.io.decode_image(img, channels=3, expand_animations=expand_animations)

        if resize:
            x = tf.image.resize(x, size=resize)

        if return_numpy:
            x = x.numpy()

        return x

    @staticmethod
    def by_plt(img):
        """
        内部其实是使用的 PIL.Image

        Args:
            img:

        Returns:

        """
        x = plt.imread(img)  # noqa
        return x


image_to_tensor = ImageTensorize.by_pil


def video_to_tensor(video_path, n_frame=None, n_step=None, resize=None, return_numpy=False, save_dir=None,
                    convert_to_rgb=True):
    """
    视频转张量

    Args:
        video_path: 视频路径
        n_frame: 按固定帧数抽帧
        n_step: 按固定间隔抽帧
        resize: 调整图像大小，格式为 (w, h)
        return_numpy: 是否整体转化为 np.array，默认为一个 list，存储每一帧的 np.array
        save_dir: 图像保存文件夹
        convert_to_rgb: 是否将通道顺序转为 'RGB'，cv2 默认的通道顺序为 'BGR'

    """
    if n_frame and n_step:
        raise ValueError('不能同时设置 n_frame 和 n_step.')

    cap = cv2.VideoCapture(video_path)
    fps = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    frames = []
    for _ in range(fps):
        ret, frame = cap.read()
        if ret:
            frames.append(frame)

    if n_frame:
        n_step = len(frames) // n_frame + 1 if len(frames) % n_frame != 0 else len(frames) // n_frame

    if n_step:
        frames = frames[::n_step] if n_step > 0 else frames

    if resize:
        frames = [cv2.resize(f, resize) for f in frames]

    if convert_to_rgb:
        frames = [cv2.cvtColor(f, cv2.COLOR_BGR2RGB) for f in frames]

    if return_numpy:
        frames = np.stack(frames)

    if save_dir:
        os.makedirs(save_dir, exist_ok=True)
        for frame_id, frame in enumerate(frames):
            cv2.imwrite(os.path.join(save_dir, '%.04d.jpg' % (frame_id + 1)), frame)

    return frames


def _test_video2tensor():
    """"""
    _video_path = r'./_test_data/v_ApplyEyeMakeup_g01_c01.avi'
    _save_dir = r'./_test_data/-out'
    _frames = video_to_tensor(_video_path, n_frame=10, resize=(224, 224), return_numpy=True, save_dir=_save_dir)
    print(_frames.shape)  # (10, 224, 224, 3)

    import matplotlib.pylab as plt

    x = _frames[0]
    # x = cv2.cvtColor(x, cv2.COLOR_BGR2RGB)
    plt.imshow(x)
    plt.show()


if __name__ == '__main__':
    """"""
    # _test_video2tensor()

    dir_path = '_test_data'
    for file_name in os.listdir(dir_path):
        file_path = os.path.join(dir_path, file_name)

        if os.path.isdir(file_path):
            continue

        is_valid = ImageCheck.is_complete(file_path)
        print('%s' % '\t'.join(str(it) for it in [file_name, is_valid]))

    ret = ImageTensorize.by_plt('./_test_data/pok.jpg')
    print(ret)