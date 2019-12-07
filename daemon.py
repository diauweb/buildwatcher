from aiohttp import web
import argparse
import os

AUTH_TOKEN = '8593EF813528FADBF0975322B41211DA8D4E4C78C25F2049AF75DA7567AC875A'

parser = argparse.ArgumentParser(description="Build updater daemon")
parser.add_argument('--path')
parser.add_argument('--port')


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
    web.run_app(app, path=args.path, port=args.port)