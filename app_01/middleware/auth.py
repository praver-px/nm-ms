from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin


class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # 将不需要登录的页面放行

        allowed_urls = ['/login/']
        if request.path_info in allowed_urls:
            return None

        # 读取session 判断是否登录过
        if not request.session.get('user'):
            # 用户未登录，重定向到登录页面
            return redirect('/login/')

        return None

        # 如果没有返回值（返回None），则继续执行下一个中间件
        # 如果有返回值 HttpResponse render redirect  则不再继续执行
        # print('M1 process_request')

    def process_response(self, request, response):
        # print('M1 process_response')
        return response
