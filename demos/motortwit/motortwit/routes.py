def setup_routes(app, handler, project_root):
    router = app.router
    h = handler
    router.add_get('/', h.timeline, name='timeline')
    router.add_get('/login', h.login_page, name='login')
    router.add_get('/logout', h.logout, name='logout')
    router.add_get('/public', h.public_timeline, name='public_timeline')
    router.add_get('/register', h.register_page, name='register')
    router.add_get('/{username}', h.user_timeline, name='user_timeline')
    router.add_get('/{username}/follow', h.follow_user, name='follow_user')
    router.add_get('/{username}/unfollow', h.unfollow_user,
                   name='unfollow_user')
    router.add_post('/add_message', h.add_message, name='add_message')
    router.add_post('/login', h.login)
    router.add_post('/register', h.register)
    router.add_static('/static/', path=str(project_root / 'static'),
                      name='static')
