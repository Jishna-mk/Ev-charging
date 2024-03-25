from django.shortcuts import redirect
def user_only(view_func):

    def wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group == 'users':
            return view_func(request, *args, **kwargs)
        else:
            return redirect('viewpage')

    return wrapper_function