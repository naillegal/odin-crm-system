from django.shortcuts import redirect
from django.urls import reverse

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Bu URL-lərə girişə icazə veririk
        allowed_urls = [reverse('index'), reverse('login')]

        # Əgər istifadəçi login olubsa və / və ya /login/ səhifəsindədirsə, task səhifəsinə yönləndir
        if request.user.is_authenticated and request.path in allowed_urls:
            return redirect('task')

        # Əgər istifadəçi login olmayıbsa və başqa səhifəyə daxil olursa, loginə yönləndir
        if not request.user.is_authenticated and request.path not in allowed_urls:
            return redirect('login')

        response = self.get_response(request)
        return response