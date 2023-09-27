import random
import time


APP_VERSION = '302.0.0.34.111'
VERSION_CODE = '208061712'

DEVICES = {
    'one_plus_7': {
        'app_version': APP_VERSION,
        'android_version': '29',
        'android_release': '10.0',
        'dpi': '420dpi',
        'resolution': '1080x2340',
        'manufacturer': 'OnePlus',
        'device': 'GM1903',
        'model': 'OnePlus7',
        'cpu': 'qcom',
        'version_code': VERSION_CODE,
    },
    'one_plus_3': {
        'app_version': APP_VERSION,
        'android_version': '28',
        'android_release': '9.0',
        'dpi': '420dpi',
        'resolution': '1080x1920',
        'manufacturer': 'OnePlus',
        'device': 'ONEPLUS A3003',
        'model': 'OnePlus3',
        'cpu': 'qcom',
        'version_code': VERSION_CODE,
    },
    # Released on March 2016
    'samsung_galaxy_s7': {
        'app_version': APP_VERSION,
        'android_version': '26',
        'android_release': '8.0',
        'dpi': '640dpi',
        'resolution': '1440x2560',
        'manufacturer': 'samsung',
        'device': 'SM-G930F',
        'model': 'herolte',
        'cpu': 'samsungexynos8890',
        'version_code': VERSION_CODE,
    },
    # Released on January 2017
    'huawei_mate_9_pro': {
        'app_version': APP_VERSION,
        'android_version': '24',
        'android_release': '7.0',
        'dpi': '640dpi',
        'resolution': '1440x2560',
        'manufacturer': 'HUAWEI',
        'device': 'LON-L29',
        'model': 'HWLON',
        'cpu': 'hi3660',
        'version_code': VERSION_CODE,
    },
    # Released on February 2018
    'samsung_galaxy_s9_plus': {
        'app_version': APP_VERSION,
        'android_version': '28',
        'android_release': '9.0',
        'dpi': '640dpi',
        'resolution': '1440x2560',
        'manufacturer': 'samsung',
        'device': 'SM-G965F',
        'model': 'star2qltecs',
        'cpu': 'samsungexynos9810',
        'version_code': VERSION_CODE,
    },
    # Released on November 2016
    'one_plus_3t': {
        'app_version': APP_VERSION,
        'android_version': '26',
        'android_release': '8.0',
        'dpi': '380dpi',
        'resolution': '1080x1920',
        'manufacturer': 'OnePlus',
        'device': 'ONEPLUS A3010',
        'model': 'OnePlus3T',
        'cpu': 'qcom',
        'version_code': VERSION_CODE,
    },
    # Released on April 2016
    'lg_g5': {
        'app_version': APP_VERSION,
        'android_version': '23',
        'android_release': '6.0.1',
        'dpi': '640dpi',
        'resolution': '1440x2392',
        'manufacturer': 'LGE/lge',
        'device': 'RS988',
        'model': 'h1',
        'cpu': 'h1',
        'version_code': VERSION_CODE,
    },
    # Released on June 2016
    'zte_axon_7': {
        'app_version': APP_VERSION,
        'android_version': '23',
        'android_release': '6.0.1',
        'dpi': '640dpi',
        'resolution': '1440x2560',
        'manufacturer': 'ZTE',
        'device': 'ZTE A2017U',
        'model': 'ailsa_ii',
        'cpu': 'qcom',
        'version_code': VERSION_CODE,
    },
    # Released on March 2016
    'samsung_galaxy_s7_edge': {
        'app_version': APP_VERSION,
        'android_version': '23',
        'android_release': '6.0.1',
        'dpi': '640dpi',
        'resolution': '1440x2560',
        'manufacturer': 'samsung',
        'device': 'SM-G935',
        'model': 'hero2lte',
        'cpu': 'samsungexynos8890',
        'version_code': VERSION_CODE,
    },
}

DEFAULT_DEVICE = DEVICES[random.choice(list(DEVICES.keys()))]


USER_AGENT_BASE =  f'Instagram {APP_VERSION} Android ({DEFAULT_DEVICE["android_version"]}/{DEFAULT_DEVICE["android_release"]}; ' + \
                   f'{DEFAULT_DEVICE["dpi"]}; {DEFAULT_DEVICE["resolution"]}; {DEFAULT_DEVICE["manufacturer"]}; ' + \
                   f'{DEFAULT_DEVICE["device"]}; {DEFAULT_DEVICE["model"]}; {DEFAULT_DEVICE["cpu"]}; en_US; {DEFAULT_DEVICE["version_code"]})'

HEADERS = {
    "X-IG-App-Locale": "fr_FR",
    "X-IG-Device-Locale": "fr_FR",
    "X-IG-Mapped-Locale": "fr_FR",
    "X-Pigeon-Rawclienttime": str(round(time.time() * 1000)),
    "X-IG-Connection-Speed": "-1kbps",
    "X-IG-Bandwidth-Speed-KBPS": str(random.randint(7000, 10000)),
    "X-IG-Bandwidth-TotalBytes-B": str(random.randint(500000, 900000)),
    "X-IG-Bandwidth-TotalTime-MS": str(random.randint(50, 150)),
    "X-IG-App-Startup-Country": "FR",
    "X-Bloks-Is-Layout-RTL": "false",
    "X-Bloks-Enable-RenderCore": "false",
    "X-IG-Connection-Type": "WIFI",
    "X-IG-Capabilities": "3brTvwM=",
    "X-FB-HTTP-Engine": "Liger",
    "X-IG-Prefetch-Request": "foreground",
    'X-IG-APP-IP': '936619743392459',
    "Accept-Language": "fr-FR",
    'Accept-Encoding': 'gzip, deflate',
    'Accept': '*/*',
    "Accept-Encoding": "gzip, deflate",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Host": "i.instagram.com",
    "Connection": "close",
    'authority': 'www.instagram.com',
    'User-Agent': USER_AGENT_BASE,
}

