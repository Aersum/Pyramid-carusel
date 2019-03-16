def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('banner', '/banner')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('view_banner', '/banner/{bannername}')
    config.add_route('add_banner', '/banner/add/{bannername}')
    config.add_route('edit_banner', '/banner/{bannername}/edit')
