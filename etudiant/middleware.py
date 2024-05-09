# from django.shortcuts import redirect
# from django.urls import reverse

# class AuthenticatedUserMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         # Check if user is authenticated
#         if request.user.is_authenticated:
#             # If user is authenticated and trying to access sign-up or login pages, redirect
#             if request.path in [reverse('sign_up_student'), reverse('login_student')]:
#                 return redirect('home_student')  # You can replace 'home' with the URL name of the page you want to redirect to
#         return self.get_response(request)