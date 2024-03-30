
<h1 align="center">Tunnel Manager</h1>

<div align="center">

[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![GitHub Issues](https://img.shields.io/github/issues/kylelobo/The-Documentation-Compendium.svg)](https://github.com/kylelobo/The-Documentation-Compendium/issues)
[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/kylelobo/The-Documentation-Compendium.svg)](https://github.com/kylelobo/The-Documentation-Compendium/pulls)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)

</div>

---

<p align="center"> A simple Python-based application to manage SSH tunnels using PyQt5. </p>

## 📝 Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)
- [Deployment](#deployment)
- [Built Using](#built_using)
- [Authors](#authors)

## 🧐 About <a name = "about"></a>

Tunnel Manager is a Python application that provides a user interface fpr WIndows to manage SSH tunnels conveniently. It allows users to start, stop, and monitor SSH tunnels easily.

## 🏁 Getting Started <a name = "getting_started"></a>

To get a copy of the project up and running on your local machine, follow these steps:

### Prerequisites

```
Windows 10+ (just tested it on 11 so far).
Ensure you have Python 3.x installed on your system.
Have the SSH connections already set up and configured.
```


### 💻 Installation

Clone the repository:

```
git clone https://github.com/tf4482/pytu.git
```

Navigate to the project directory:

```
cd pytu
```

Install the required dependencies:

```
pip install -r requirements.txt
```

## 🔧 Configuration

```
Define your connections in pytu.json

      {
        "name": "Tunnel 1",
        "ssh": {
          "port": 12345,
          "options": ["-f", "-N"],
          "forwardings": [
            {
              "local_port": 8001,
              "remote_host": "localhost",
              "remote_port": 8000
            },
            {
              "local_port": 3307,
              "remote_host": "localhost",
              "remote_port": 3306
            }
          ],
          "host": "192.168.1.100"
        }
      },
```

## 🎈 Usage <a name="usage"></a>

To use the application, simply run the Python script `pytu.py`. This will launch the Tunnel Manager user interface, where you can start, stop, and monitor SSH tunnels.

## 🚀 Deployment <a name = "deployment"></a>

For deploying this application on a live system, you can follow standard Python deployment procedures.

## ⛏️ Built Using <a name = "built_using"></a>

- [Python](https://www.python.org/) - Programming Language
- [PyQt5](https://riverbankcomputing.com/software/pyqt/intro) - GUI Framework
- [psutil](https://github.com/giampaolo/psutil) - Process Utilities
- [subprocess](https://docs.python.org/3/library/subprocess.html) - Subprocess Management

## Screenshots 📸

![image](https://github.com/tf4482/pytu/assets/107394980/f3608356-9db6-4972-8fa2-b6b215f068db) ![image](https://github.com/tf4482/pytu/assets/107394980/f8b3e71e-66b2-4630-82ae-74e1e3ef4dac) ![image](https://github.com/tf4482/pytu/assets/107394980/937a0524-04b0-4537-95db-7e5d41a8e73d)

## ✍️ Authors <a name = "authors"></a>

- [@tf4482](https://github.com/tf4482) - Developer

## License 📜

Distributed under the MIT License. See LICENSE for more information.

**Project Link:** [https://github.com/tf482/improvo](https://github.com/tf482/improvo)

