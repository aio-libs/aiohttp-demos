def setup_routes(app, handler, project_root):
    add_route = app.router.add_route
    add_route('GET', '/', handler.timeline, name='timeline')
    add_route('GET', '/public',
              handler.public_timeline, name='public_timeline')
    add_route('GET', '/logout', handler.logout, name='logout')

    add_route('GET', '/login', handler.login_page, name='login')
    add_route('POST', '/login', handler.login)

    add_route('GET', '/register', handler.register_page, name='register')
    add_route('POST', '/register', handler.register)
    add_route('GET', '/{username}', handler.user_timeline,
              name='user_timeline')
    add_route('GET', '/{username}/follow', handler.follow_user,
              name='follow_user')
    add_route('GET', '/{username}/unfollow', handler.unfollow_user,
              name='unfollow_user')
    add_route('POST', '/add_message', handler.add_message,
              name='add_message')
    app.router.add_static('/static/',
                          path=str(project_root / 'static'),
                          name='static')
