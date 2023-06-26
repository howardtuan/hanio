from .models import member, Manager

class MemberNameMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        MAccount = request.session.get('MAccount')
        Name = None
        is_manager = False
        if MAccount:
            try:
                user = member.objects.get(MAccount=MAccount)
                Name = user.MName
            except member.DoesNotExist:
                # 尝试从管理者表中获取
                try:
                    manager = Manager.objects.get(username=MAccount)
                    Name = manager.name
                    is_manager = True
                except Manager.DoesNotExist:
                    pass

        # 将会员或管理者的名字添加到请求上下文中
        request.Name = Name
        request.is_manager = is_manager

        response = self.get_response(request)
        return response
