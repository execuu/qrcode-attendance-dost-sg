class GroupMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            return self.get_response(request)
        groups = request.user.groups.values_list('name', flat=True)
        request.group_membership = {
            'Officer': 'Officers' in groups, 
            'Member': 'Members' in groups
        }
        return self.get_response(request)
