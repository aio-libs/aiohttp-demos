from aiohttpdemo_blog.views import index, login, logout, create_post


def setup_routes(app):
    app.router.add_get('/', index, name='index')
    app.router.add_get('/login', login, name='login')
    app.router.add_post('/login', login, name='login')
    app.router.add_get('/logout', logout, name='logout')
    app.router.add_get('/create', create_post, name='create-post')
    app.router.add_post('/create', create_post, name='create-post')
