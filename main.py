import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout


def main():
    app = QApplication(sys.argv)

    window = QWidget()
    window.setWindowTitle("HB Tools - Test")
    window.setGeometry(100, 100, 400, 300)

    layout = QVBoxLayout()
    label = QLabel("Hello World - HB Tools IDE")
    layout.addWidget(label)

    window.setLayout(layout)
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
