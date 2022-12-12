import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QGridLayout, QHBoxLayout,QVBoxLayout
from PyQt5.QtCore import Qt, QUrl, QEvent
from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineSettings, QWebEngineView

video_list = ['raTMa8MneTY', 'gt-v_YCkaMY', 'el_9_e6DoHw']

class YoutubePlayer(QWidget):
    counter = 0
    def __init__(self, video_id, parent=None):
        super().__init__()
        self.parent = parent
        self.video_id = video_id

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        topLayout = QHBoxLayout()
        self.layout.addLayout(topLayout)

        label = QLabel('Enter Video Id:')
        self.input = QLineEdit()
        self.input.installEventFilter(self)
        self.input.setText(self.video_id)

        topLayout.addWidget(label,1)
        topLayout.addWidget(self.input,9)
        #設定video id
        self.AddWebView(video_list[self.counter])

        # button
        buttonLayout = QHBoxLayout()
        self.layout.addLayout(buttonLayout)

        buttonUpdate = QPushButton('Update', clicked = self.updateVideo)
        buttonRemove = QPushButton('Delete', clicked = self.removePlayer)
        buttonLayout.addWidget(buttonUpdate)
        buttonLayout.addWidget(buttonRemove)

    def eventFilter(self, source, event):
        if event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Return:
                self.updateVideo()
        return super().eventFilter(source, event)

    
    def AddWebView(self, video_id):
        self.webview = QWebEngineView()
        self.webview.setUrl(QUrl(f'https://www.youtube.com/embed/{self.video_id}?rel=0'))
        self.layout.addWidget(self.webview)

    def updateVideo(self):
        self.counter += 1
        video_id = video_list[self.counter]
        self.webview.setUrl(QUrl(f'https://www.youtube.com/embed/{self.video_id}?rel=0'))
        


    def removePlayer(self):
        widget = self.sender().parent()
        widget.setParent(None)
        widget.deleteLater()

    def orginizeLayout(self):
        playerCount = self.parent.videoGrid.count()
        players = []

        for i in reversed(range(playerCount)): 
            player = self.parent.videoGrid.itemAt(i).widget()
            players.append(player)

        for indx, player in enumerate(players[::-1]):
            self.parent.videoGrid.addWidget(player, indx%3, indx//3)

class YoutubeWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Media Player')
        self.setWindowIcon(QIcon('paper.png'))
        self.setMinimumSize(1800,800)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.videoGrid = QGridLayout()
        self.layout.addLayout(self.videoGrid)

        self.player = YoutubePlayer('raTMa8MneTY',parent=self)
        self.videoGrid.addWidget(self.player,0,0)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = YoutubeWindow()
    window.show()

    sys.exit(app.exec_())