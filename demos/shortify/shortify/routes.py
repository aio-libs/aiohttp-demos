from shortify.views import index, redirect, shortify


def setup_routes(app, project_root):
    router = app.router
    router.add_get('/', index, name='index')
    router.add_get('/{short_id}', redirect, name='short')
    router.add_post('/shortify', shortify, name='shortify')
    router.add_static(
        '/static/', path=str(project_root / 'static'),
        name='static')
