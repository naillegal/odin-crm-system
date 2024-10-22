from django.shortcuts import redirect
from django.urls import reverse

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # İcazə verilən URL-lərin başlanğıcı
        allowed_prefixes = [
            reverse('index'),   # index səhifəsi
            reverse('login'),   # login səhifəsi
            '/salescontractdetail/',  
            '/assistpricedetail/',
        ]

        # İstifadəçi login olubsa və əsas səhifəyə (/ və ya /login/) daxil olursa
        if request.user.is_authenticated and request.path in [reverse('index'), reverse('login')]:
            return redirect('task')  # İstifadəçini task səhifəsinə yönləndir

        # Əgər istifadəçi login olmadan qadağan olunmuş səhifəyə daxil olursa
        if not request.user.is_authenticated and not any(
            request.path.startswith(prefix) for prefix in allowed_prefixes
        ):
            return redirect('login')  # Login səhifəsinə yönləndir

        response = self.get_response(request)
        return response
