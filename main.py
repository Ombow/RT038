import os
import pandas as pd
from datetime import datetime
import calendar
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.core.window import Window

# Mengatur latar belakang aplikasi agar tampak modern & bersih (Abu-abu terang)
Window.clearcolor = (0.95, 0.96, 0.98, 1)

# File Database Lokal
DB_FILE = "database_warga_rt038.csv"

# Fungsi Menghitung Usia Lengkap secara Otomatis (Tahun, Bulan, Hari)
def hitung_usia_lengkap(tgl_lahir_str):
    try:
        birth_date = datetime.strptime(str(tgl_lahir_str).strip(), "%d-%m-%Y")
        today = datetime.today()
        
        years = today.year - birth_date.year
        months = today.month - birth_date.month
        days = today.day - birth_date.day
        
        if days < 0:
            months -= 1
            prev_month = today.month - 1 if today.month > 1 else 12
            prev_year = today.year if today.month > 1 else today.year - 1
            days += calendar.monthrange(prev_year, prev_month)[1]
            
        if months < 0:
            years -= 1
            months += 12
            
        return f"{years} Tahun {months} Bulan {days} Hari"
    except:
        return "0 Tahun 0 Bulan 0 Hari"

# Inisialisasi Database CSV jika belum ada
if not os.path.exists(DB_FILE):
    df = pd.DataFrame(columns=[
        "Alamat", "No_Rumah", "Nama", "No_Telp", "Jenis_Kelamin", 
        "Status_Nikah", "Status_Tempat_Tinggal", "Pendidikan", "Agama", "Tanggal_Lahir", "Usia_Lengkap"
    ])
    df.to_csv(DB_FILE, index=False)

# Komponen Header Logo dengan Ukuran Setengah Halaman (Sangat Besar)
class HeaderLogo(BoxLayout):
    def __init__(self, **kwargs):
        super(HeaderLogo, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = 400  # Logo diperbesar menjadi setengah halaman
        self.spacing = 10
        self.padding = [10, 10, 10, 10]
        
        if os.path.exists("logo_rt.png"):
            self.add_widget(Image(source="logo_rt.png", size_hint_y=None, height=320))
        else:
            self.add_widget(Label(text="[ Logo RT 038 RW 008 ]", font_size=30, color=(0.5,0.5,0.5,1)))
        
        self.add_widget(Label(
            text="DATABASE WARGA RT 038 / RW 008", 
            font_size=30, 
            bold=True, 
            color=(0.1, 0.2, 0.4, 1),
            size_hint_y=None,
            height=60
        ))

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        main_layout.add_widget(HeaderLogo())
        
        card_layout = BoxLayout(orientation='vertical', padding=15, spacing=20)
        self.pass_input = TextInput(hint_text="🔑 Kata Sandi Admin", password=True, multiline=False, size_hint_y=None, height=75, font_size=30)
        card_layout.add_widget(self.pass_input)
        
        btn_admin = Button(text="🚀 Masuk Admin", background_normal='', background_color=(0.12, 0.53, 0.90, 1), size_hint_y=None, height=75, bold=True, font_size=30)
        btn_admin.bind(on_press=self.login_admin)
        card_layout.add_widget(btn_admin)
        
        btn_guest = Button(text="👀 Masuk Tamu", background_normal='', background_color=(0.35, 0.65, 0.35, 1), size_hint_y=None, height=75, bold=True, font_size=30)
        btn_guest.bind(on_press=self.login_guest)
        card_layout.add_widget(btn_guest)
        
        main_layout.add_widget(card_layout)
        self.add_widget(main_layout)

    def login_admin(self, instance):
        if self.pass_input.text == "123000":
            App.get_running_app().is_admin = True
            self.manager.current = "menu"
        else:
            self.show_popup("Akses Ditolak", "Kata Sandi Admin Salah!")

    def login_guest(self, instance):
        App.get_running_app().is_admin = False
        self.manager.current = "menu"

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message, color=(1,1,1,1), font_size=30), size_hint=(0.8, 0.3))
        popup.open()

class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        layout.add_widget(HeaderLogo())
        
        layout.add_widget(Label(text="PILIHAN MENU UTAMA", font_size=30, bold=True, color=(0.2, 0.2, 0.2, 1), size_hint_y=None, height=50))
        
        self.btn_tambah = Button(text="➕ Tambah Data Warga", background_normal='', background_color=(0.95, 0.60, 0.10, 1), size_hint_y=None, height=75, bold=True, font_size=30)
        self.btn_tambah.bind(on_press=self.goto_tambah)
        layout.add_widget(self.btn_tambah)
        
        btn_lihat = Button(text="📊 Lihat Data & Laporan", background_normal='', background_color=(0.15, 0.45, 0.65, 1), size_hint_y=None, height=75, bold=True, font_size=30)
        btn_lihat.bind(on_press=self.goto_lihat)
        layout.add_widget(btn_lihat)
        
        btn_logout = Button(text="🚪 Keluar / Ganti Akun", background_normal='', background_color=(0.80, 0.25, 0.25, 1), size_hint_y=None, height=75, bold=True, font_size=30)
        btn_logout.bind(on_press=self.logout)
        layout.add_widget(btn_logout)
        
        self.add_widget(layout)

    def on_enter(self):
        if not App.get_running_app().is_admin:
            self.btn_tambah.disabled = True
            self.btn_tambah.background_color = (0.7, 0.7, 0.7, 1)
            self.btn_tambah.text = "🔒 Tambah (Terkunci)"
        else:
            self.btn_tambah.disabled = False
            self.btn_tambah.background_color = (0.95, 0.60, 0.10, 1)
            self.btn_tambah.text = "➕ Tambah Data Warga"

    def goto_tambah(self, instance):
        self.manager.current = "tambah"

    def goto_lihat(self, instance):
        self.manager.current = "lihat"

    def logout(self, instance):
        self.manager.current = "login"

class TambahScreen(Screen):
    def __init__(self, **kwargs):
        super(TambahScreen, self).__init__(**kwargs)
        layout = GridLayout(cols=2, padding=15, spacing=12)
        
        # Semua ukuran huruf (font_size) pada label, input, dan spinner diatur ke 30
        layout.add_widget(Label(text="Alamat Rumah:", color=(0.2,0.2,0.2,1), bold=True, font_size=30))
        self.alamat = TextInput(multiline=False, font_size=30)
        layout.add_widget(self.alamat)
        
        layout.add_widget(Label(text="No Rumah:", color=(0.2,0.2,0.2,1), bold=True, font_size=30))
        self.no_rumah = TextInput(multiline=False, font_size=30)
        layout.add_widget(self.no_rumah)
        
        layout.add_widget(Label(text="Nama Lengkap:", color=(0.2,0.2,0.2,1), bold=True, font_size=30))
        self.nama = TextInput(multiline=False, font_size=30)
        layout.add_widget(self.nama)
        
        layout.add_widget(Label(text="No Telp / HP:", color=(0.2,0.2,0.2,1), bold=True, font_size=30))
        self.no_telp = TextInput(hint_text="08123456789", multiline=False, font_size=30)
        layout.add_widget(self.no_telp)
        
        layout.add_widget(Label(text="Jenis Kelamin:", color=(0.2,0.2,0.2,1), bold=True, font_size=30))
        self.jk = Spinner(text='Laki-laki', values=('Laki-laki', 'Perempuan'), font_size=30)
        layout.add_widget(self.jk)
        
        layout.add_widget(Label(text="Status Pernikahan:", color=(0.2,0.2,0.2,1), bold=True, font_size=30))
        self.status = Spinner(text='Belum Menikah', values=('Belum Menikah', 'Menikah', 'Janda', 'Duda'), font_size=30)
        layout.add_widget(self.status)
        
        layout.add_widget(Label(text="Tempat Tinggal:", color=(0.2,0.2,0.2,1), bold=True, font_size=30))
        self.status_tinggal = Spinner(text='Warga Tetap', values=('Warga Tetap', 'Kontrak', 'Kos'), font_size=30)
        layout.add_widget(self.status_tinggal)
        
        layout.add_widget(Label(text="Pendidikan:", color=(0.2,0.2,0.2,1), bold=True, font_size=30))
        self.pendidikan = Spinner(text='SMA', values=('SD', 'SMP', 'SMA', 'D3', 'S1', 'S2', 'Lainnya'), font_size=30)
        layout.add_widget(self.pendidikan)
        
        layout.add_widget(Label(text="Agama:", color=(0.2,0.2,0.2,1), bold=True, font_size=30))
        self.agama = Spinner(text='Islam', values=('Islam', 'Kristen', 'Katolik', 'Hindu', 'Buddha', 'Konghucu'), font_size=30)
        layout.add_widget(self.agama)
        
        layout.add_widget(Label(text="Tgl Lahir (DD-MM-YYYY):", color=(0.2,0.2,0.2,1), bold=True, font_size=30))
        self.tgl_lahir = TextInput(hint_text="31-12-1990", multiline=False, font_size=30)
        layout.add_widget(self.tgl_lahir)
        
        btn_simpan = Button(text="💾 Simpan", background_normal='', background_color=(0.15, 0.65, 0.25, 1), bold=True, font_size=30)
        btn_simpan.bind(on_press=self.simpan_data)
        layout.add_widget(btn_simpan)
        
        btn_kembali = Button(text="⬅ Kembali", background_normal='', background_color=(0.5, 0.5, 0.5, 1), bold=True, font_size=30)
        btn_kembali.bind(on_press=self.kembali)
        layout.add_widget(btn_kembali)
        
        self.add_widget(layout)

    def simpan_data(self, instance):
        if not all([self.alamat.text, self.no_rumah.text, self.nama.text, self.tgl_lahir.text]):
            self.show_popup("Peringatan", "Kolom utama wajib diisi!")
            return
            
        usia_otomatis = hitung_usia_lengkap(self.tgl_lahir.text)
        
        new_data = {
            "Alamat": self.alamat.text,
            "No_Rumah": self.no_rumah.text,
            "Nama": self.nama.text,
            "No_Telp": self.no_telp.text,
            "Jenis_Kelamin": self.jk.text,
            "Status_Nikah": self.status.text,
            "Status_Tempat_Tinggal": self.status_tinggal.text,
            "Pendidikan": self.pendidikan.text,
            "Agama": self.agama.text,
            "Tanggal_Lahir": self.tgl_lahir.text,
            "Usia_Lengkap": usia_otomatis
        }
        
        df = pd.read_csv(DB_FILE)
        df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
        df.to_csv(DB_FILE, index=False)
        
        self.show_popup("Sukses", f"Data warga berhasil disimpan!\nUsia: {usia_otomatis}")
        self.manager.current = "menu"

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message, color=(1,1,1,1), font_size=30), size_hint=(0.8, 0.3))
        popup.open()

    def kembali(self, instance):
        self.manager.current = "menu"

class LihatScreen(Screen):
    def __init__(self, **kwargs):
        super(LihatScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=15, spacing=12)
        
        layout.add_widget(HeaderLogo())
        
        self.info_label = Label(text="Memuat Data...", font_size=30, color=(0.2,0.2,0.2,1), bold=True)
        layout.add_widget(self.info_label)
        
        btn_excel = Button(text="📥 Download Excel (.xlsx)", background_normal='', background_color=(0.12, 0.53, 0.30, 1), size_hint_y=None, height=75, bold=True, font_size=30)
        btn_excel.bind(on_press=self.export_excel)
        layout.add_widget(btn_excel)
        
        btn_pdf = Button(text="📄 Download Laporan PDF", background_normal='', background_color=(0.75, 0.25, 0.25, 1), size_hint_y=None, height=75, bold=True, font_size=30)
        btn_pdf.bind(on_press=self.export_pdf)
        layout.add_widget(btn_pdf)
        
        btn_kembali = Button(text="⬅ Kembali ke Menu", background_normal='', background_color=(0.5, 0.5, 0.5, 1), size_hint_y=None, height=75, bold=True, font_size=30)
        btn_kembali.bind(on_press=self.kembali)
        layout.add_widget(btn_kembali)
        
        self.add_widget(layout)

    def on_enter(self):
        self.hitung_laporan()

    def hitung_laporan(self):
        if not os.path.exists(DB_FILE) or os.stat(DB_FILE).st_size == 0:
            self.info_label.text = "Belum ada data warga terdaftar."
            return
            
        df = pd.read_csv(DB_FILE)
        total_warga = len(df)
        
        today = datetime.today()
        anak_kecil, remaja, orang_tua, lansia = 0, 0, 0, 0
        
        for tgl in df['Tanggal_Lahir']:
            try:
                birth_date = datetime.strptime(str(tgl).strip(), "%d-%m-%Y")
                age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
                if age <= 12:
                    anak_kecil += 1
                elif 13 <= age <= 21:
                    remaja += 1
                elif 22 <= age <= 59:
                    orang_tua += 1
                else:
                    lansia += 1
            except:
                pass
                
        janda = len(df[df['Status_Nikah'] == 'Janda'])
        duda = len(df[df['Status_Nikah'] == 'Duda'])
        
        tetap = len(df[df['Status_Tempat_Tinggal'] == 'Warga Tetap'])
        kontrak = len(df[df['Status_Tempat_Tinggal'] == 'Kontrak'])
        kos = len(df[df['Status_Tempat_Tinggal'] == 'Kos'])
        
        text_laporan = (
            f"📋 REKAPITULASI DATA WARGA RT 038 / RW 008\n\n"
            f"• Total Seluruh Warga : {total_warga} Orang\n"
            f"• Anak-anak (0-12 thn) : {anak_kecil} | Remaja (13-21 thn) : {remaja}\n"
            f"• Orang Tua (22-59 thn) : {orang_tua} | Lansia (60+ thn) : {lansia}\n"
            f"• Janda : {janda} orang   |   Duda : {duda} orang\n\n"
            f"🏠 Status Tempat Tinggal:\n"
            f"  - Tetap : {tetap}  |  Kontrak : {kontrak}  |  Kos : {kos}"
        )
        self.info_label.text = text_laporan

    def export_excel(self, instance):
        if os.path.exists(DB_FILE):
            excel_path = "/sdcard/Download/Data_Warga_RT038.xlsx"
            df = pd.read_csv(DB_FILE)
            df.to_excel(excel_path, index=False)
            self.show_popup("Berhasil", f"Excel tersimpan di:\n{excel_path}\nSiap dibagikan ke WhatsApp!")

    def export_pdf(self, instance):
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.pdfgen import canvas
            
            pdf_path = "/sdcard/Download/Laporan_RT038.pdf"
            c = canvas.Canvas(pdf_path, pagesize=letter)
            c.drawString(50, 750, "Laporan Data Warga RT 038 RW 008")
            
            df = pd.read_csv(DB_FILE)
            y = 720
            for index, row in df.iterrows():
                text = f"{row['Alamat']} No.{row['No_Rumah']} - {row['Nama']} (Usia: {row.get('Usia_Lengkap','-')})"
                c.drawString(50, y, text)
                y -= 20
                if y < 50:
                    c.showPage()
                    y = 750
            c.save()
            self.show_popup("Berhasil", f"PDF tersimpan di:\n{pdf_path}\nSiap dibagikan ke WhatsApp!")
        except Exception as e:
            self.show_popup("Error", f"Gagal membuat PDF: {str(e)}")

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message, color=(1,1,1,1), font_size=30), size_hint=(0.8, 0.3))
        popup.open()

    def kembali(self, instance):
        self.manager.current = "menu"

class MyApp(App):
    is_admin = False
    
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(TambahScreen(name='tambah'))
        sm.add_widget(LihatScreen(name='lihat'))
        return sm

if __name__ == '__main__':
    MyApp().run()