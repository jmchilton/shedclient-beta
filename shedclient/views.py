

def install(request):
    _check_install_request(request)
    map(_handle_install())


def _check_install_request(request):
    if not isinstance(request, list):
        raise ValueError("Install request requires list of one or more repositories to install.")
