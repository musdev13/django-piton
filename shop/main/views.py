from django.core.exceptions import ValidationError
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from .models import Mod
from .services import create_user


def main(request):
    mods = Mod.objects.prefetch_related('tags').all()
    return render(request, 'main/index.html', {'mods': mods})


def about(request):
    return render(request, 'main/about.html')


def mod_detail(request, mod_id):
    mod = get_object_or_404(Mod.objects.prefetch_related('tags'), pk=mod_id)
    return render(request, 'main/mod_detail.html', {'mod': mod})


def search(request):
    query = request.GET.get('q', '').strip()
    results = Mod.objects.none()
    if query:
        results = (
            Mod.objects.prefetch_related('tags')
            .filter(
                Q(name__icontains=query)
                | Q(description__icontains=query)
                | Q(slug__icontains=query)
                | Q(category__icontains=query)
                | Q(tags__name__icontains=query)
            )
            .distinct()
        )
    return render(request, 'main/search.html', {'query': query, 'mods': results})


def register(request):
    return render(request, 'main/register.html')


def register_submit(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST only'}, status=405)

    try:
        user = create_user(
            username=request.POST.get('username', '').strip(),
            email=request.POST.get('email', '').strip(),
            password=request.POST.get('password', ''),
            avatar=request.FILES.get('avatar'),
        )
    except ValidationError as exc:
        return JsonResponse({'error': '; '.join(exc.messages)}, status=400)

    return JsonResponse({
        'message': 'ok',
        'username': user.username,
        'email': user.email,
    })
