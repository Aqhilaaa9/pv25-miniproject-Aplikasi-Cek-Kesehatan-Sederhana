from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.uic import loadUi
import sys

class HealthChecker(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("Project Mini.ui", self)

        self.setWindowTitle("Aplikasi Cek Kesehatan Sederhana")

        # Validasi widget dari UI
        required_widgets = [
            'inputNama', 'inputBerat', 'spinUmur', 'slider_tinggi',
            'label_tinggi', 'radio_ya', 'radio_tidak', 'combo_aktivitas',
            'btn_cek', 'output_result'
        ]
        for widget in required_widgets:
            if not hasattr(self, widget):
                print(f"⚠️  UI Error: '{widget}' tidak ditemukan di UI file!")

        # Tambahkan flag untuk cek apakah slider sudah digeser
        self.slider_digeser = False
        self.slider_tinggi.valueChanged.connect(self.slider_changed)

        self.btn_cek.clicked.connect(self.check_health)
        self.output_result.hide()

        if hasattr(self, 'actionTentang_Aplikasi'):
            self.actionTentang_Aplikasi.triggered.connect(self.show_about)
        else:
            print("⚠️  Peringatan: 'actionTentang_Aplikasi' tidak ditemukan di UI!")

    def slider_changed(self):
        self.slider_digeser = True
        self.label_tinggi.setText(f"{self.slider_tinggi.value()} cm")

    def check_health(self):
        nama = self.inputNama.text().strip()
        berat = self.inputBerat.text().strip()
        umur = self.spinUmur.value()
        tinggi = self.slider_tinggi.value()
        merokok_ya = self.radio_ya.isChecked()
        merokok_tidak = self.radio_tidak.isChecked()
        aktivitas = self.combo_aktivitas.currentText()

        if not nama:
            QMessageBox.warning(self, "Peringatan", "Nama tidak boleh kosong!")
            return
        if not berat:
            QMessageBox.warning(self, "Peringatan", "Berat tidak boleh kosong!")
            return
        try:
            berat = float(berat)
        except ValueError:
            QMessageBox.warning(self, "Peringatan", "Berat harus berupa angka!")
            return
        if umur == 0:
            QMessageBox.warning(self, "Peringatan", "Umur belum diisi!")
            return
        if not self.slider_digeser:
            QMessageBox.warning(self, "Peringatan", "Tinggi badan belum diatur!")
            return
        if not (merokok_ya or merokok_tidak):
            QMessageBox.warning(self, "Peringatan", "Silakan pilih status merokok!")
            return
        if aktivitas == "-- Pilih --":
            QMessageBox.warning(self, "Peringatan", "Silakan pilih aktivitas fisik!")
            return

        tinggi_meter = tinggi / 100
        bmi = berat / (tinggi_meter ** 2)

        if bmi < 18.5:
            bmi_category = "Kurang Berat Badan"
            bmi_saran = "Perhatikan asupan makanan yang bergizi."
        elif bmi < 24.9:
            bmi_category = "Normal"
            bmi_saran = "Pertahankan gaya hidup sehat Anda!"
        elif bmi < 29.9:
            bmi_category = "Kelebihan Berat Badan"
            bmi_saran = "Cobalah untuk menurunkan berat badan dengan diet dan olahraga."
        else:
            bmi_category = "Obesitas"
            bmi_saran = "Konsultasikan dengan dokter untuk program penurunan berat badan."

        merokok = merokok_ya
        saran = []

        if umur > 40:
            saran.append("Rutin periksa kesehatan.")
        if merokok:
            saran.append("Disarankan untuk mengurangi atau menghentikan kebiasaan merokok untuk menjaga kesehatan paru-paru dan mencegah risiko penyakit kronis seperti kanker dan penyakit jantung.")
        else:
            saran.append("Pertahankan rutinitas aktivitas fisik Anda agar kesehatan tubuh tetap terjaga dan risiko penyakit dapat diminimalkan.")

        status = "SEHAT" if not merokok and aktivitas == "Rutin" and umur < 40 else "PERLU PERHATIAN"
        color = "#2ecc71" if status == "SEHAT" else "#e74c3c"

        self.output_result.setStyleSheet(f"color: {color}; font-weight: bold;")
        self.output_result.setText(
            f"Halo, {nama}!\n"
            f"Status kesehatan Anda: {status}\n"
            f"BMI Anda: {bmi:.2f} ({bmi_category})\n\n"
            f"Saran:\n" + "\n".join(saran) + "\n\n"
            f"Catatan BMI: {bmi_saran}"
        )
        self.output_result.show()

    def show_about(self):
        QMessageBox.information(
            self, "Tentang",
            "Aplikasi ini dikembangkan untuk memberikan evaluasi awal terhadap status kesehatan pengguna berdasarkan sejumlah data pribadi yang diinputkan."
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HealthChecker()
    window.show()
    sys.exit(app.exec_())
