#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -------------------------------------------

# 自动处理nginx配置
import argparse
from pathlib import Path
import requests

default_nginx_config_str = '''server
{{
    listen {listen};
    server_name {server_name};
    index index.html index.htm default.htm default.html;
    root /www/wwwroot/{file_root};
    location ~ ^/(\.user.ini|\.htaccess|\.git|\.svn|\.project|LICENSE|README.md)
    {{
        return 404;
    }}
    #一键申请SSL证书验证目录相关设置
    location ~ \.well-known{{
        allow all;
    }}
    location ~ .*\.(gif|jpg|jpeg|png|bmp|swf)$
    {{
        expires      30d;
        error_log /dev/null;
        access_log /dev/null;
    }}
    location ~ .*\.(js|css)?$
    {{
        expires      12h;
        error_log /dev/null;
        access_log /dev/null; 
    }}
}}
'''


parser = argparse.ArgumentParser(description='自动处理nginx配置')
parser.add_argument('l', type=str, help='listen 配置')
parser.add_argument('--sn', type=str, help='server_name 配置')
parser.add_argument('fr', type=str, help='file_root 配置')

args = parser.parse_args()

# path = Path('.')
path = Path('/www/server/panel/vhost/nginx')

if not path.exists():
    exit('无法获取写入路径')

path = path / f'{args.fr}.conf'
if not args.sn:
    args.sn = requests.get('http://ifconfig.me/ip', timeout=1).text.strip()

conf = default_nginx_config_str.format(listen=args.l, server_name=args.sn, file_root=args.fr)
with path.open('w+') as f:
    f.write(conf)
