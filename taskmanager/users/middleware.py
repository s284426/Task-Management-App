class AdminMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and request.user.is_admin:
            if not request.user.is_staff or not request.user.is_superuser:
                request.user.is_staff = True
                request.user.is_superuser = True
                request.user.save()
        return self.get_response(request)