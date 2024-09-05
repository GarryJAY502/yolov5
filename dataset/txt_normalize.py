import os
from PIL import Image


def is_normalized(data):
    """
    判断给定的坐标是否已经归一化，即坐标值是否都在 [0, 1] 范围内。

    :param data: YOLO 格式的数据 [class_id, x_center, y_center, width, height]
    :return: 如果坐标已经归一化则返回 True，否则返回 False
    """
    x_center = float(data[1])
    y_center = float(data[2])
    width = float(data[3])
    height = float(data[4])

    return 0 <= x_center <= 1 and 0 <= y_center <= 1 and 0 <= width <= 1 and 0 <= height <= 1


def normalize_yolo_labels(label_path, img_dir):
    """
    归一化 YOLO 标签，将像素单位的坐标转换为 [0, 1] 范围，并检查是否已归一化。

    :param label_path: 标签文件的路径
    :param img_dir: 图片所在的目录
    """
    # 遍历所有的标签文件
    for label_file in os.listdir(label_path):
        if not label_file.endswith('.txt'):
            continue

        # 对应的图片文件
        image_file = label_file.replace('.txt', '.jpg')  # 假设图片格式是 .jpg，如果不同需修改

        image_path = os.path.join(img_dir, image_file)
        label_file_path = os.path.join(label_path, label_file)

        if not os.path.exists(image_path):
            print(f"找不到对应的图片文件: {image_file}")
            continue

        # 获取图片的宽高
        with Image.open(image_path) as img:
            img_width, img_height = img.size

        # 读取标签文件，检查是否已归一化
        normalized_labels = []
        needs_normalization = False
        with open(label_file_path, 'r') as f:
            lines = f.readlines()
            for line in lines:
                data = line.strip().split()
                if not is_normalized(data):
                    # 如果没有归一化，进行归一化处理
                    class_id = int(data[0])
                    x_center = float(data[1]) / img_width
                    y_center = float(data[2]) / img_height
                    width = float(data[3]) / img_width
                    height = float(data[4]) / img_height
                    normalized_labels.append(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")
                    needs_normalization = True
                else:
                    # 已经归一化的标签直接保留
                    normalized_labels.append(line)

        # 如果需要归一化，则更新标签文件
        if needs_normalization:
            with open(label_file_path, 'w') as f:
                f.writelines(normalized_labels)
            print(f"归一化完成: {label_file_path}")
        else:
            print(f"已归一化: {label_file_path}")


# 设置标签文件路径和图片文件路径
label_dir = 'aircraft/Annotation/labels'  # 标签文件夹路径
image_dir = 'aircraft/images/'  # 图片文件夹路径

# 归一化标签
normalize_yolo_labels(label_dir, image_dir)
