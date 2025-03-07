import tkinter as tk
from tkinter import messagebox
import win32com.client
import hashlib
import socket
import sys
import os
import logging
from datetime import datetime

class FileBlocker:
    def __init__(self):
        self.syslog_server = "localhost"  # Verander dit naar uw syslog server
        self.syslog_port = 514  # Standaard syslog poort
        
        # Maak een map voor de logs in ProgramData
        self.log_dir = os.path.join(os.environ.get('PROGRAMDATA', 'C:\\ProgramData'), 'FileBlocker')
        os.makedirs(self.log_dir, exist_ok=True)
        
        # Configureer logging
        logging.basicConfig(
            filename=os.path.join(self.log_dir, 'file_blocker.log'),
            level=logging.WARNING,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
    def get_file_info(self, filepath):
        """Haal bestandsinformatie op"""
        if not filepath or not os.path.exists(filepath):
            raise FileNotFoundError(f"Bestand niet gevonden: {filepath}")
            
        filename = os.path.basename(filepath)
        with open(filepath, 'rb') as f:
            file_hash = hashlib.sha1(f.read()).hexdigest()
        ip_address = socket.gethostbyname(socket.gethostname())
        return filename, file_hash, ip_address

    def send_to_syslog(self, message):
        """Stuur bericht naar log bestand"""
        try:
            logging.warning(message)
        except Exception as e:
            print(f"Fout bij loggen: {e}")

    def show_warning(self, filepath):
        """Toon waarschuwingsvenster"""
        try:
            filename, file_hash, ip_address = self.get_file_info(filepath)
        except FileNotFoundError as e:
            messagebox.showerror("Fout", str(e))
            return
            
        # Maak het hoofdvenster
        root = tk.Tk()
        root.title("Bestand geblokkeerd")
        root.geometry("400x300")
        
        # Voorkom dat het venster geminimaliseerd of gemaximaliseerd kan worden
        root.resizable(False, False)
        
        # Maak het venster modaal door het altijd bovenop te houden
        root.attributes('-topmost', True)
        
        # Voeg een waarschuwingsicoon en bericht toe
        warning_label = tk.Label(root, text="⚠️", font=("Arial", 48))
        warning_label.pack(pady=10)
        
        message = f"Dit bestand is geblokkeerd vanwege veiligheidsredenen.\n\n"
        message += f"Bestandsnaam: {filename}\n"
        message += f"SHA1 Hash: {file_hash}\n"
        message += f"IP Adres: {ip_address}\n"
        message += f"Tijdstip: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        message_label = tk.Label(root, text=message, wraplength=350)
        message_label.pack(pady=10)
        
        # Stuur informatie naar syslog
        log_message = f"Geblokkeerd bestand: {filename} | Hash: {file_hash} | IP: {ip_address}"
        self.send_to_syslog(log_message)
        
        # Sluit knop
        close_button = tk.Button(root, text="Sluiten", command=root.destroy)
        close_button.pack(pady=20)
        
        # Bind de sluitknop aan het venster
        root.protocol("WM_DELETE_WINDOW", root.destroy)
        
        # Start de GUI loop
        root.mainloop()

def register_file_association():
    """Registreer de applicatie voor .js bestanden"""
    try:
        shell = win32com.client.Dispatch("WScript.Shell")
        # Registreer voor .js bestanden
        key = shell.RegWrite("HKEY_CURRENT_USER\\Software\\Classes\\.js\\", "JSFile.Blocker", "REG_SZ")
        key = shell.RegWrite("HKEY_CURRENT_USER\\Software\\Classes\\JSFile.Blocker\\shell\\open\\command\\", 
                           f'"{os.path.abspath(sys.executable)}" "{os.path.abspath(__file__)}" "%1"', "REG_SZ")
        return True
    except Exception as e:
        print(f"Fout bij registreren bestandsassociatie: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1]:
        # Als er een bestand is meegegeven, toon de waarschuwing
        blocker = FileBlocker()
        blocker.show_warning(sys.argv[1])
    elif "--register" in sys.argv:
        # Alleen registreren als --register argument is meegegeven
        if register_file_association():
            print("Bestandsassociatie succesvol geregistreerd!")
        else:
            print("Fout bij registreren bestandsassociatie.")
    else:
        print("Gebruik: python file_blocker.py [bestand] of python file_blocker.py --register") 