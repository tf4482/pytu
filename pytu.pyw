import sys
import json
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout
from PyQt5.QtCore import QThread, pyqtSignal
from functools import partial
import psutil
import subprocess
import time


def debug_print(message):
    if "debug" in sys.argv:
        print(message)


def get_ssh_processes():
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        if proc.info['name'] == 'ssh.exe':
            yield proc


def process_matches_command_line(proc, command_lines):
    proc_cmdline = ' '.join(proc.info['cmdline'])
    return any(cl in proc_cmdline for cl in command_lines)


def kill_process(proc):
    try:
        proc.kill()
        proc.wait()
        debug_print(f"Process {proc.pid} (ssh.exe) successfully terminated.")
        return True
    except psutil.NoSuchProcess:
        debug_print(f"Process {proc.pid} not found.")
    except Exception as e:
        debug_print(f"Error terminating process {proc.pid}: {e}")
    return False


def start_application(app):
    startupinfo = None
    if "debug" not in sys.argv:
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
    proc = subprocess.Popen(
        app['command'], shell=True, startupinfo=startupinfo)
    time.sleep(1)
    return proc.pid


class TunnelManagerWorker(QThread):
    update_signal = pyqtSignal(int, str)

    def __init__(self, tunnels):
        super().__init__()
        self.tunnels = tunnels
        self.tunnel_statuses = [False] * len(tunnels)

    def run(self):
        while True:
            existing_ssh_processes = list(get_ssh_processes())
            for idx, tunnel in enumerate(self.tunnels):
                tunnel_active = any(process_matches_command_line(
                    proc, [tunnel['command']]) for proc in existing_ssh_processes)
                self.tunnel_statuses[idx] = tunnel_active
                self.update_signal.emit(
                    idx, f"Status: {'Active' if tunnel_active else 'Inactive'}")
            time.sleep(1)


class TunnelManagerUI(QWidget):
    def __init__(self, tunnels):
        super().__init__()

        self.tunnels = tunnels

        self.create_ui()
        self.worker = TunnelManagerWorker(self.tunnels)
        self.worker.update_signal.connect(self.update_status)
        self.worker.start()

        self.setWindowTitle("python tunneler")

    def create_ui(self):
        self.btn_start_all = QPushButton("Start All", self)
        self.btn_start_all.clicked.connect(self.start_all_tunnels)

        self.btn_stop_all = QPushButton("Stop All", self)
        self.btn_stop_all.clicked.connect(self.stop_all_tunnels)

        layout = QVBoxLayout()
        layout.addWidget(self.btn_start_all)
        layout.addWidget(self.btn_stop_all)

        self.status_labels = []
        for idx, tunnel in enumerate(self.tunnels):
            tunnel['command'] = f'ssh -p {tunnel["ssh"]["port"]} {" ".join(tunnel["ssh"]["options"])} {" ".join(f"-L {forward['local_port']}:{forward['remote_host']}:{
                forward['remote_port']}" for forward in tunnel["ssh"]["forwardings"])} {tunnel["ssh"]["user"]}@{tunnel["ssh"]["host"]}'
            start_func = partial(self.start_tunnel, idx)
            stop_func = partial(self.stop_tunnel, idx)

            btn_start = QPushButton(f"Start {tunnel['name']}", self)
            btn_start.clicked.connect(start_func)

            btn_stop = QPushButton(f"Stop {tunnel['name']}", self)
            btn_stop.clicked.connect(stop_func)

            status_label = QLabel("Status: -", self)
            layout.addWidget(status_label)
            layout.addWidget(btn_start)
            layout.addWidget(btn_stop)
            self.status_labels.append(status_label)

        self.setLayout(layout)
        self.setMinimumWidth(255)

    def start_tunnel(self, idx):
        start_application(self.tunnels[idx])

    def stop_tunnel(self, idx):
        existing_ssh_processes = list(get_ssh_processes())
        for proc in existing_ssh_processes:
            if process_matches_command_line(proc, [self.tunnels[idx]['command']]):
                kill_process(proc)
                return
        print(f"No active process found for {self.tunnels[idx]['name']}.")

    def start_all_tunnels(self):
        for idx, tunnel in enumerate(self.tunnels):
            self.start_tunnel(idx)

    def stop_all_tunnels(self):
        existing_ssh_processes = list(get_ssh_processes())
        for proc in existing_ssh_processes:
            if process_matches_command_line(proc, [tunnel['command'] for tunnel in self.tunnels]):
                kill_process(proc)

    def update_status(self, idx, status):
        status_label = self.status_labels[idx]
        status_label.setText(status)
        if "Active" in status:
            status_label.setStyleSheet("color: green")
        else:
            status_label.setStyleSheet("color: red")


if __name__ == "__main__":
    with open("pytu.json", "r") as file:
        data = json.load(file)
        tunnels = data['tunnels']

    app = QApplication(sys.argv)
    tunnel_manager_ui = TunnelManagerUI(tunnels)
    tunnel_manager_ui.show()
    sys.exit(app.exec_())
