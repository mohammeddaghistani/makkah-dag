import customtkinter as ctk
from tkinter import messagebox, filedialog
import threading
import logging
import time

# إعداد نظام تسجيل الأخطاء
logging.basicConfig(filename='app_log.txt', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

class MakkahApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # إعدادات النافذة الرئيسية
        self.title("Makkah Dag Development - النسخة المطورة")
        self.geometry("700x500")
        ctk.set_appearance_mode("System") 
        ctk.set_default_color_theme("blue")

        # بناء واجهة المستخدم
        self.setup_ui()

    def setup_ui(self):
        # العنوان الرئيسي
        self.label = ctk.CTkLabel(self, text="نظام مكة داغ لمعالجة البيانات", font=("Segoe UI", 24, "bold"))
        self.label.pack(pady=30)

        # حاوية الإدخال
        self.frame = ctk.CTkFrame(self)
        self.frame.pack(pady=10, padx=40, fill="x")

        self.entry = ctk.CTkEntry(self.frame, placeholder_text="اكتب نصاً أو اختر ملفاً للبدء...", width=400)
        self.entry.pack(side="left", padx=10, pady=20)

        self.btn_browse = ctk.CTkButton(self.frame, text="استعراض..", width=100, command=self.browse_file)
        self.btn_browse.pack(side="right", padx=10)

        # أزرار التحكم
        self.btn_run = ctk.CTkButton(self, text="بدء التنفيذ"، font=("Segoe UI", 16), command=self.start_process_thread, fg_color="#2c3e50", hover_color="#34495e")
        self.btn_run.pack(pady=20)

        # شريط التقدم
        self.progress = ctk.CTkProgressBar(self, width=500)
        self.progress.pack(pady=10)
        self.progress.set(0)

        # منطقة الرسائل
        self.status_label = ctk.CTkLabel(self, text="الحالة: جاهز"، font=("Segoe UI", 13))
        self.status_label.pack(side="bottom", pady=20)

    def browse_file(self):
        filename = filedialog.askopenfilename()
        if filename:
            self.entry.delete(0, 'end')
            self.entry.insert(0, filename)

    def start_process_thread(self):
        # فحص المدخلات قبل البدء
        if not self.entry.get():
            messagebox.showwarning("تنبيه", "الرجاء إدخال نص أو اختيار ملف أولاً")
            return
            
        thread = threading.Thread(target=self.run_logic, daemon=True)
        thread.start()

    def run_logic(self):
        try:
            self.btn_run.configure(state="disabled")
            self.status_label.configure(text="الحالة: جاري المعالجة...")
            self.progress.start()

            # --- هنا يتم تنفيذ منطق البرنامج ---
            # مثال لعملية معالجة:
            input_val = self.entry.get()
            time.sleep(2) # محاكاة معالجة بيانات ثقيلة
            
            # تسجيل العملية
            logging.info(f"تمت معالجة البيانات: {input_val}")
            
            # تحديث الواجهة عند الانتهاء
            self.progress.stop()
            self.progress.set(1)
            self.status_label.configure(text="الحالة: تم الإنجاز بنجاح")
            messagebox.showinfo("نجاح", "تمت المهمة وتحديث السجلات بنجاح")

        except Exception as e:
            logging.error(f"Error: {str(e)}")
            messagebox.showerror("خطأ", f"حدث خطأ: {e}")
            self.status_label.configure(text="الحالة: فشلت العملية")
        finally:
            self.btn_run.configure(state="normal")

if __name__ == "__main__":
    app = MakkahApp()
    app.mainloop()
