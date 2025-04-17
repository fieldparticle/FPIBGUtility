import sys
from PyQt6.QtWidgets import (
    QTabWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QWidget,
    QSlider,
    QLabel,
    QFileDialog,
    QApplication,
)
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtCore import Qt, QUrl, QTimer, QTime

class TabRunRpt(QTabWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def Create(self, FPIBGBase):
        self.bobj = FPIBGBase
        self.cfg = self.bobj.cfg.config
        self.log = self.bobj.log.log

        #Define needed components
        self.media_player = QMediaPlayer()
        self.video_widget = QVideoWidget()
        self.play_button = QPushButton("Play")
        self.pause_button = QPushButton("Pause")
        self.stop_button = QPushButton("Stop")
        self.progress_slider = QSlider(Qt.Orientation.Horizontal)
        self.current_time_label = QLabel("00:00")
        self.total_time_label = QLabel(" / 00:00")
        self.open_button = QPushButton("Open Video")

        #########################
        ### Create the Layout ###
        #########################
        main_layout = QVBoxLayout()

        #Add main video box
        self.video_widget.setStyleSheet("background-color: black;")
        main_layout.addWidget(self.video_widget)

        #Add Control layout
        controls_layout = QHBoxLayout()
        play_pause_layout = QHBoxLayout()
        play_pause_layout.addWidget(self.play_button)
        play_pause_layout.addWidget(self.pause_button)
        play_pause_layout.addWidget(self.stop_button)
        controls_layout.addLayout(play_pause_layout)
        controls_layout.addWidget(self.progress_slider)
        #Add time labels
        time_layout = QHBoxLayout()
        time_layout.addWidget(self.current_time_label)
        time_layout.addWidget(self.total_time_label)
        controls_layout.addLayout(time_layout)
        main_layout.addLayout(controls_layout)

        #Open Button
        main_layout.addWidget(self.open_button)

        #########################
        ### Add Functionality ###
        #########################
        #Define settings for layout
        self.setLayout(main_layout)

        #Add functionality to buttons
        self.open_button.clicked.connect(self.open_video)
        self.play_button.clicked.connect(self.play_video)
        self.pause_button.clicked.connect(self.pause_video)
        self.stop_button.clicked.connect(self.stop_video)
        self.pause_button.setEnabled(False)
        self.stop_button.setEnabled(False)
        self.progress_slider.setEnabled(False)

        #Set media player functionality
        self.media_player.playbackStateChanged.connect(self.media_state_changed)
        self.media_player.positionChanged.connect(self.position_changed)
        self.media_player.durationChanged.connect(self.duration_changed)
        self.progress_slider.sliderMoved.connect(self.set_position)
        self.media_player.setVideoOutput(self.video_widget)

        self.current_video_path = ""
        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_time_labels)

    def open_video(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            self, "Open Video File", "", "Video Files (*.mp4 *.avi *.mov *.mkv *)"
        )
        if file_path:
            self.current_video_path = file_path
            self.media_player.setSource(QUrl.fromLocalFile(file_path))
            self.play_button.setEnabled(True)
            self.stop_button.setEnabled(False) # Enable stop only after a file is loaded
            self.progress_slider.setEnabled(True)
            self.total_time_label.setText(" / 00:00")
            self.current_time_label.setText("00:00")
            self.progress_slider.setValue(0)
        return
    def play_video(self):
        if self.media_player.mediaStatus() == QMediaPlayer.MediaStatus.NoMedia:
            if self.current_video_path:
                self.media_player.setSource(QUrl.fromLocalFile(self.current_video_path))
            else:
                self.open_video()
                return

        self.media_player.play()
        self.play_button.setEnabled(False)
        self.pause_button.setEnabled(True)
        self.stop_button.setEnabled(True)
        self.timer.start()
        return
    def pause_video(self):
        self.media_player.pause()
        self.play_button.setEnabled(True)
        self.pause_button.setEnabled(False)
        self.timer.stop()
        return
    def stop_video(self):
        self.media_player.stop()
        self.play_button.setEnabled(True)
        self.pause_button.setEnabled(False)
        self.stop_button.setEnabled(False)
        self.progress_slider.setValue(0)
        self.current_time_label.setText("00:00")
        self.timer.stop()
        return
    def media_state_changed(self, state):
        if state == QMediaPlayer.PlaybackState.PlayingState:
            self.play_button.setEnabled(False)
            self.pause_button.setEnabled(True)
        elif state == QMediaPlayer.PlaybackState.PausedState:
            self.play_button.setEnabled(True)
            self.pause_button.setEnabled(False)
        elif state == QMediaPlayer.PlaybackState.StoppedState:
            self.play_button.setEnabled(True)
            self.pause_button.setEnabled(False)
            self.stop_button.setEnabled(False)
            self.progress_slider.setValue(0)
            self.current_time_label.setText("00:00")
            self.timer.stop()
        elif state == QMediaPlayer.MediaStatus.EndOfMedia:
            self.play_button.setEnabled(True)
            self.pause_button.setEnabled(False)
            self.media_player.setPosition(0)
            self.progress_slider.setValue(0)
            self.current_time_label.setText("00:00")
            self.timer.stop()
        return
    def position_changed(self, position):
        self.progress_slider.setValue(position)
        self.update_time_labels(position)
        return
    def duration_changed(self, duration):
        self.progress_slider.setRange(0, duration)
        total_time = QTime(0, 0, 0).addMSecs(duration)
        self.total_time_label.setText(f" / {total_time.toString('mm:ss')}")
        return
    def set_position(self, position):
        self.media_player.setPosition(position)
        self.update_time_labels(position)
        return
    def update_time_labels(self, current_position=None):
        if current_position is None:
            current_position = self.media_player.position()
        current_time = QTime(0, 0, 0).addMSecs(current_position)
        self.current_time_label.setText(current_time.toString("mm:ss"))
        return

