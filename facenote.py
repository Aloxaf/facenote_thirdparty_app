import json
from pathlib import Path
from mitmproxy import ctx, http

APP_LIST = {
    "code": 0,
    "msg": "",
    "body": {
        "list": [
            {
                "id": 0,
                "name": "创建快捷方式",
                "icon": "",
                "appVersion": "V1.17",
                "appSize": "0.9MB",
                "appName": "com.x7890.shortcutcreator",
                "appDesc": "",
            },
            {
                "id": 1,
                "name": "APK 安装器",
                "icon": "",
                "appVersion": "V3.5",
                "appSize": "2.8MB",
                "appName": "com.tokyonth.installer",
                "appDesc": "",
            },
            {
                "id": 2,
                "name": "MiXplorer",
                "icon": "",
                "appVersion": "V6.57.6",
                "appSize": "3.2MB",
                "appName": "com.mixplorer",
                "appDesc": "",
            },
        ],
        "page": {"currentPage": 1, "pageSize": 10, "totalPage": 1, "totalRecord": 3},
    },
}


def make_app_info(name):
    return json.dumps({
        "body": {
            "appUrl": f"http://example.com?download={name}",
        },
        "code": 0,
        "msg": ""
    })


def get_apk(name):
    return open(Path(__file__).parent / "apk" / f"{name}.zip", "rb").read()


class MoreApp:
    def __init__(self):
        pass

    def request(self, flow: http.HTTPFlow):
        query = flow.request.query
        if query.get("ca") == "Eink_AppStore.AppList":
            flow.response = http.Response.make(200, json.dumps(APP_LIST))
        elif query.get("ca") == "Eink_AppStore.AppInfo":
            flow.response = http.Response.make(200, make_app_info(query["appName"]))
        elif query.get("download"):
            flow.response = http.Response.make(200, get_apk(query.get("download")))


addons = [MoreApp()]
