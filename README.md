# Python WinPrint 

Python WinPrint consists of two major components; server and client. Server receives the print requests via Redis server, which acts as a queue server, together with the file uploaded via HTTP POST from the client. The client currently can only prints pdf file. Hence the user has to convert any file format to pdf format before using the client to send the print job.

## Sypnosis
This is a small tool created when the author faced difficulty of printing when the linux/mac os driver is not available for his OS platform. Hence with the limited resource in hand, he created a printer server on Windows, which allows him to send print jobs via Redis Server to print his document.

### Installation
There are few steps to set up both server and client (Note: Please follow the following sequence):

- Client (Ubuntu 16.04)

    - **git clone this repo**

        ```git
        git clone https://github.com/tangingw/python_winprint.git
        ```
    - **on the directory ~/python_winprint, type the following command**
        ```bash
        SHELL>mkdir ~/print_dir
        SHELL>cd ~/python_winprint
        SHELL>make install_ubuntu
        ```
        this will install the necessary library and setup a redis server on your computer

    - **Configure Redis server**
        - Change the following line in /etc/redis/redis.conf
        
        ```conf
        bind 127.0.0.1
        ```
        to 
        ```conf
        bind 0.0.0.0
        ```
    - **Restart the Redis server**
        ```bash
        SHELL>sudo service restart redis-server
        ```
    - **Edit _~/python_winprint/config/config.json_**

        1. Change the _CLIENT -> PRINT_PATH_ to _/home/<YOUR_USERNAME>/print_dir/_
        2. Change the _REDIS_SERVER_ to your host IP address

        ```json
        {
            "SERVER": {
                "PRINT_PATH": "C:\\Users\\<YOUR WIN_ID>\\test_upload\\"
            },
            "CLIENT":{
                "PRINT_PATH": "/home/<YOUR_USERNAME>/print_dir/"
            },
            "UPLOAD_URL": "http://<YOUR FLASK APP IP>:5000/upload",
            "REDIS_SERVER": "<YOUR HOST IP ADDRESS>"
        }
        ```

- Server (Windows 8.x, Windows 10, Windows Server 2012 R2)
    - **Prepare a Windows Machine**
        - You can either use a physical Windows machine or virtual machine (both laptop and desktop and make sure you have a legal copy of Windows). The author uses Windows Server 2012 R2, virtual machine hosted in KVM.  

    - **Install your printer driver on Windows Machine**
        - Without this, the print_server.py will not work. Make sure you do a test print after you have installed your printer driver so that it will not cause any issue to printer_server.py

    - **Install [python 3.x](https://www.python.org/downloads/windows/) on your Windows machine**
        - Currently print_server.py is coded in python 3.x since the author wants to learn python 3.x.

    - **Install latest copy of [Adobe Reader](https://get.adobe.com/reader/otherversions/)**
    - **git clone this repo**
        ```git
        git clone https://github.com/tangingw/python_winprint.git
        ```
    - **Install necessary library**
        ```git
        pip install win32compat win32core win32ext redis flask
        ```
    - **Edit _config.json_ in C:\Users\\<YOUR_WIN_ID>\python_winprint\config folder**
        ```json
        {
            "SERVER": {
                "PRINT_PATH": "C:\\Users\\<YOUR WIN_ID>\\test_upload\\"
            },
            "CLIENT":{
                "PRINT_PATH": "/var/print/"
            },
            "UPLOAD_URL": "http://<YOUR FLASK APP IP>:5000/upload",
            "REDIS_SERVER": "<YOUR REDIS IP>"
        }
        ```
    - **Start your application in [Powershell](https://docs.microsoft.com/en-us/powershell/scripting/getting-started/getting-started-with-windows-powershell?view=powershell-5.1)**
        ```powershell
        POWER_SHELL> cd .\python_winprint\
        POWER_SHELL> python print_server.py
        ```

### How to print

_print_client.py_ mimics the famous unix printing command, _lpr_, hence shares some similar positional parameters.

- Print the whole document
    ```bash
    SHELL>~/python_winprint/print_client.py foo_bar.pdf
    ```
- Print single page, e.g. page 10 only
    ```bash
    SHELL>~/python_winprint/print_client.py foo_bar.pdf 10-10 
    ```
- Print multiple pages, e.g. from 200 to 214
    ```bash
    SHELL>~/python_winprint/print_client.py foo_bar.pdf 200-214
    ```

### To Do

- Add authentication system
- Add a database system to capture the print records. The print records are currently stored in Redis Server
