import sys
from PyQt6.QtWidgets import QApplication, QFileDialog, QVBoxLayout, QHBoxLayout, QWidget
from PyQt6.QtCore import Qt
from qfluentwidgets import (PushButton, SubtitleLabel, BodyLabel, 
                            CardWidget, InfoBar, InfoBarPosition, ProgressBar)
import pandas as pd

class SuccessIndexApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('College Success Indexer')
        self.resize(900, 600)
        self.setStyleSheet("background-color: #f9f9f9;") # Light gray background

        # Layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(40, 40, 40, 40)
        self.layout.setSpacing(20)

        # 1. Header Card
        self.header_card = CardWidget(self)
        self.header_layout = QVBoxLayout(self.header_card)
        
        self.title = SubtitleLabel('Upload Raw Excel Sheet', self)
        self.subtitle = BodyLabel('Support for First Year and Direct Second Year differentiation', self)
        
        self.header_layout.addWidget(self.title)
        self.header_layout.addWidget(self.subtitle)
        self.header_layout.setContentsMargins(20, 20, 20, 20)
        
        self.layout.addWidget(self.header_card)

        # 2. Action Area
        self.upload_btn = PushButton('Select Excel File', self)
        self.upload_btn.clicked.connect(self.upload_file)
        self.layout.addWidget(self.upload_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        # 3. Progress Bar (Hidden initially)
        self.progress = ProgressBar(self)
        self.progress.setValue(0)
        self.progress.hide()
        self.layout.addWidget(self.progress)

        # 4. Results Area
        self.result_label = BodyLabel('', self)
        self.layout.addWidget(self.result_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.layout.addStretch()

    def upload_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Excel", "", "Excel Files (*.xlsx)")
        
        if file_path:
            self.process_logic(file_path)

    def process_logic(self, file_path):
        # SHOW LOADING
        self.progress.show()
        self.progress.setValue(30)
        
        try:
            # --- YOUR PANDAS LOGIC HERE ---
            df = pd.read_excel(file_path)
            
            # Example Logic: Count rows
            total_students = len(df)
            
            # Mocking the separation logic
            # regular = df[df['Enrollment'].str.startswith('22')]
            
            self.progress.setValue(100)
            
            # Show Success Message
            InfoBar.success(
                title='Processing Complete',
                content=f"Successfully analyzed {total_students} students.",
                orient=Qt.Orientation.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self
            )
            
            self.result_label.setText(f"File Loaded: {file_path.split('/')[-1]}")
            
        except Exception as e:
            InfoBar.error(
                title='Error',
                content=str(e),
                parent=self
            )

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SuccessIndexApp()
    window.show()
    sys.exit(app.exec())