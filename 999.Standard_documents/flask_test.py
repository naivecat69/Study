import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout
)

class SimpleGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # 창 제목 / 크기
        self.setWindowTitle("PyQt 간단 예제")
        self.resize(300, 150)

        # 위젯 생성
        self.label = QLabel("버튼을 눌러보세요", self)
        self.button = QPushButton("클릭", self)

        # 버튼 이벤트 연결
        self.button.clicked.connect(self.on_click)

        # 레이아웃
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def on_click(self):
        self.label.setText("버튼이 눌렸습니다!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SimpleGUI()
    window.show()
    sys.exit(app.exec_())
