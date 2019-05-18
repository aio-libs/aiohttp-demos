def setup_main_handler(app, handler):
    app.router.add_post(
        "/listen",
        handler.listen_message,
        name="listen",
    )
