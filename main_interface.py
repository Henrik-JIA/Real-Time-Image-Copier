from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QSlider, QCheckBox, QProgressBar, QComboBox, QFileDialog, QGridLayout, QHBoxLayout
from PyQt5.QtCore import Qt
import sys
# from Real_time_copy_images import real_time_add_images
import real_time_add_images

class Dialog(QDialog):
    def __init__(self):
        super(Dialog, self).__init__()

        self.setWindowTitle("实时复制图片")
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setModal(True)  # 设置为模态对话框
        layout = QGridLayout()

        # 原图片文件夹
        self.src_dir_entry = QLineEdit()
        browse_src_dir_button = QPushButton("浏览")
        browse_src_dir_button.clicked.connect(self.browse_src_dir)
        layout.addWidget(QLabel("原图片文件夹"), 0, 0)
        layout.addWidget(self.src_dir_entry, 0, 1)
        layout.addWidget(browse_src_dir_button, 0, 2)

        # 目标图片文件夹
        self.dst_dir_entry = QLineEdit()
        browse_dst_dir_button = QPushButton("浏览")
        browse_dst_dir_button.clicked.connect(self.browse_dst_dir)
        layout.addWidget(QLabel("输出图片文件夹"), 1, 0)
        layout.addWidget(self.dst_dir_entry, 1, 1)
        layout.addWidget(browse_dst_dir_button, 1, 2)

        # 需要同时复制的图片数量
        self.n_slider = QSlider(Qt.Horizontal)
        self.n_slider.setMinimum(1)
        self.n_slider.setMaximum(10)
        self.n_slider.valueChanged.connect(self.update_slider_label)
        self.n_label = QLabel()
        self.update_slider_label(self.n_slider.value())
        layout.addWidget(QLabel("同时复制的图片数量"), 2, 0)
        slider_layout = QHBoxLayout()
        slider_layout.addWidget(self.n_slider)
        slider_layout.addWidget(self.n_label)
        layout.addLayout(slider_layout, 2, 1)

        # 拷贝时间间隔
        self.t_combobox = QComboBox()
        self.t_combobox.addItems([str(i) for i in range(500, 5001, 500)])
        layout.addWidget(QLabel("拷贝时间间隔"), 3, 0)
        layout.addWidget(self.t_combobox, 3, 1)

        # 选择线程数
        self.threads_combobox = QComboBox()
        self.threads_combobox.addItems([str(i) for i in range(1, 11)])
        layout.addWidget(QLabel("选择线程数"), 4, 0)
        layout.addWidget(self.threads_combobox, 4, 1)

        # KML经纬度范围
        self.use_kml_checkbutton = QCheckBox("KML经纬度范围")
        self.kml_path_entry = QLineEdit()
        browse_kml_file_button = QPushButton("浏览")
        browse_kml_file_button.clicked.connect(self.browse_kml_file)
        layout.addWidget(self.use_kml_checkbutton, 5, 0)
        layout.addWidget(self.kml_path_entry, 5, 1)
        layout.addWidget(browse_kml_file_button, 5, 2)

        # 是否需要写入end空文件
        self.write_end_file_checkbutton = QCheckBox("写入end空文件")
        layout.addWidget(self.write_end_file_checkbutton, 6, 0)

        # 进度条
        self.progress = QProgressBar()
        layout.addWidget(self.progress, 7, 0, 1, 3)
        
        # 连接进度信号到进度条
        real_time_add_images.signal_holder.progress_signal.connect(self.progress.setValue)

        # 运行按钮
        run_button = QPushButton("运行")
        run_button.clicked.connect(self.run_function)
        run_button.setMinimumWidth(100)  # 设置最小宽度
        layout.addWidget(run_button, 8, 1, 1, 1, Qt.AlignRight)  # 右对齐

        # 关闭按钮
        cancel_button = QPushButton("关闭")
        cancel_button.clicked.connect(self.close)
        cancel_button.setMinimumWidth(100)  # 设置最小宽度
        layout.addWidget(cancel_button, 8, 2, 1, 1, Qt.AlignRight)  # 右对齐

        self.setLayout(layout)

    def update_slider_label(self, value):
        self.n_label.setText(str(value))

    def browse_src_dir(self):
        dir_path = QFileDialog.getExistingDirectory(self, "选择文件夹")
        self.src_dir_entry.setText(dir_path)

    def browse_dst_dir(self):
        dir_path = QFileDialog.getExistingDirectory(self, "选择文件夹")
        self.dst_dir_entry.setText(dir_path)

    def browse_kml_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择文件", "", "KML files (*.kml)")
        self.kml_path_entry.setText(file_path)

    def run_function(self):
        print("运行按钮被点击了")
        # 在这里添加你的函数实现
        # 从界面获取参数
        src_dir = self.src_dir_entry.text()
        dst_dir = self.dst_dir_entry.text()
        n = self.n_slider.value()
        t = int(self.t_combobox.currentText())
        threads = int(self.threads_combobox.currentText())
        use_kml = self.use_kml_checkbutton.isChecked()
        kml_path = self.kml_path_entry.text() if use_kml else None
        end = self.write_end_file_checkbutton.isChecked()

        # 调用核心处理算法
        real_time_add_images.real_time_main(src_dir, dst_dir, kml_path, use_kml, n, t, threads, end, self.progress)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    dialog = Dialog()
    dialog.show()

    sys.exit(app.exec_())