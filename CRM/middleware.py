from django.shortcuts import redirect
from django.urls import reverse

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Login olmadan giriş icazəsi olan URL-lərin başlanğıcı
        allowed_prefixes = [
            reverse('index'),
            reverse('login'),
            '/salescontractdetail/',  
            '/assistpricedetail/',
        ]

        # İstifadəçi login olmadan icazəsiz səhifəyə daxil olursa
        if not request.user.is_authenticated and not any(
            request.path.startswith(prefix) for prefix in allowed_prefixes
        ):
            return redirect('login')

        response = self.get_response(request)
        return response
