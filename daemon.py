#!/usr/bin/python3

from aiohttp import web
import argparse
import os

AUTH_TOKEN = None

parser = argparse.ArgumentParser(description="Build updater daemon")
parser.add_argument('--path' )
parser.add_argument('--port' )
parser.add_argument('--token')


async def built(request):
    pas = request.match_info['pass']
    if pas != AUTH_TOKEN: 
        return web.json_response({'result': 'auth_failure'})
    retval = os.system('sh ./script.sh')
    
    return web.json_response({'result':  'ok' if retval == 0 else 'err', 'value': retval})

 
if __name__ == '__main__':
    app = web.Application()
    app.add_routes([web.get('/notifier/build_ok/{pass}', built)])
    
    args = parser.parse_args()

    if args.token is None:
        if not os.path.isfile('./TOKEN'):
            print('No predefined token!')
            exit()
        else: 
            with open('./TOKEN','r') as f:
                AUTH_TOKEN = f.readline()
    else: AUTH_TOKEN = args.token

    web.run_app(app, path=args.path, port=args.port)