import piexif
import piexif.helper
from PIL import Image
import json


class ImgExif:
    """
    longitude：经度
    latitude；维度
    altitude：海拔高度
    focal_length：相机焦距

    carrier_pitch_angle: 载机俯仰角 （绕x轴旋转,机头与水平的夹角，水平为零，机头冲上为正，冲下为负）
    carrier_roll_angle: 载机横滚角 （绕y轴旋转,机身水平为零右倾为正，左倾为负(没有时发送0)）
    carrier_yaw_angle: 载机偏航角 （绕z轴旋转,[0-360],机头指向正北为零，机头指向北偏东为正，北偏西为负）

    pitch_frame_angle: 俯仰框架角 （绕x轴旋转,上正下负）
    roll_frame_angle: 横滚框架角 （绕y轴旋转,左滚为负，右滚为正）
    bearing_frame_angle: 方位框架角 （绕z轴旋转,±180,左负右正）

    relative_height: 相对高度，相对地面的高度
    """

    def __init__(self):
        self.width = None
        self.height = None
        self.focal_length = None
        self.longitude = None
        self.latitude = None
        self.altitude = None
        self.relative_height = None
        self.frame_roll_angle = None
        self.frame_pitch_angle = None
        self.frame_bearing_angle = None
        self.carrier_roll_angle = None
        self.carrier_pitch_angle = None
        self.carrier_yaw_angle = None

    def read_gps(self, image_path):
        """读取图像中的GPS信息"""
        img = Image.open(image_path)
        exif_dict = piexif.load(img.info['exif'])
        
        # read gps info
        lng_info = exif_dict['GPS'][piexif.GPSIFD.GPSLongitude]
        lat_info = exif_dict['GPS'][piexif.GPSIFD.GPSLatitude]
        alt_info = exif_dict['GPS'][piexif.GPSIFD.GPSAltitude]

        self.longitude = lng_info[0][0] / lng_info[0][1] \
                         + lng_info[1][0] / (lng_info[1][1] * 60) \
                         + lng_info[2][0] / (lng_info[2][1] * 3600)
        self.latitude = lat_info[0][0] / lat_info[0][1] \
                        + lat_info[1][0] / (lat_info[1][1] * 60) \
                        + lat_info[2][0] / (lat_info[2][1] * 3600)
        self.altitude = alt_info[0] / alt_info[1]

    def read_exif(self, image_path):
        """读取图像中的exif信息"""
        img = Image.open(image_path)
        exif_dict = piexif.load(img.info['exif'])

        self.width = img.width
        self.height = img.height

        # read gps info
        self.read_gps(image_path)

        # read focal length
        focal_length_info = exif_dict['Exif'][piexif.ExifIFD.FocalLength]
        self.focal_length = focal_length_info[0] / focal_length_info[1]

        # read camera pose info
        try:
            user_comment = exif_dict["Exif"].get(piexif.ExifIFD.UserComment)
            if user_comment:
                img_user_comment = piexif.helper.UserComment.load(user_comment)
                camera_pose_info = json.loads(img_user_comment)
                # 读取相机姿态信息
                self.frame_roll_angle = camera_pose_info.get('roll_frame_angle')
                self.frame_pitch_angle = camera_pose_info.get('pitch_frame_angle')
                self.frame_bearing_angle = camera_pose_info.get('bearing_frame_angle')
                self.carrier_roll_angle = camera_pose_info.get('carrier_roll_angle')
                self.carrier_pitch_angle = camera_pose_info.get('carrier_pitch_angle')
                self.carrier_yaw_angle = camera_pose_info.get('carrier_yaw_angle')
                self.relative_height = camera_pose_info.get('relative_height')
            else:
                print('UserComment 不存在！')
        except KeyError:
            print('UserComment 字段不存在！')
        except json.JSONDecodeError:
            print('UserComment 不是有效的 JSON 格式！')
        except Exception as e:
            print(f'读取相机姿态信息时发生错误: {e}')

    def print_img_exif(self):
        print("longitude:{}".format(self.longitude))
        print("latitude:{}".format(self.latitude))
        print("altitude:{}".format(self.altitude))
        print("focal_length:{}".format(self.focal_length))
        print("roll_frame_angle:{}".format(self.frame_roll_angle))
        print("pitch_frame_angle:{}".format(self.frame_pitch_angle))
        print("bearing_frame_angle:{}".format(self.frame_bearing_angle))
        print("carrier_roll_angle:{}".format(self.carrier_roll_angle))
        print("carrier_pitch_angle:{}".format(self.carrier_pitch_angle))
        print("carrier_yaw_angle:{}".format(self.carrier_yaw_angle))
        print("relative_height:{}".format(self.relative_height))