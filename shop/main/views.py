import json

from django.http import Http404, JsonResponse
from django.shortcuts import render

MODS = [
    {
        'id': 1,
        'slug': 'sodium',
        'name': 'Sodium',
        'logo': 'main/img/sodium-logo.webp',
        'description': (
            'Оптимізаційний мод, що переписує рушій рендерингу Minecraft: '
            'суттєво підвищує FPS, зменшує мікрозатримки та споживання пам\'яті '
            'без втрати якості зображення.'
        ),
        'category': 'Performance',
        'mc_version': '1.20+',
        'downloads': '50M+',
        'features': [
            'Переписаний рушій рендерингу на основі OpenGL',
            'Суттєвий приріст FPS на слабких ПК',
            'Сумісність з більшістю популярних шейдерів',
        ],
    },
    {
        'id': 2,
        'slug': 'create',
        'name': 'Create',
        'logo': 'main/img/create-logo.webp',
        'description': (
            'Технічний мод про обертові механізми, шестерні, конвеєри та складну '
            'автоматизацію з впізнаваним естетичним стилем у дусі стімпанку.'
        ),
        'category': 'Technology',
        'mc_version': '1.18+',
        'downloads': '20M+',
        'features': [
            'Сотні нових блоків для автоматизації',
            'Унікальна кінетична механіка (обертання, передачі)',
            'Естетичний стиль у дусі стімпанку',
        ],
    },
    {
        'id': 3,
        'slug': 'iris',
        'name': 'Iris Shaders',
        'logo': 'main/img/iris-logo.webp',
        'description': (
            'Легкий та швидкий завантажувач шейдерів із підтримкою пакетів для '
            'OptiFine та повною сумісністю з Sodium — красива гра без просідань FPS.'
        ),
        'category': 'Shaders',
        'mc_version': '1.19+',
        'downloads': '15M+',
        'features': [
            'Повна сумісність із Sodium',
            'Підтримка OptiFine-шейдерів "з коробки"',
            'Мінімальний вплив на FPS',
        ],
    },
]


def main(request):
    return render(request, 'main/index.html', {'mods': MODS})


def about(request):
    return render(request, 'main/about.html')


def mod_detail(request, mod_id):
    mod = next((m for m in MODS if m['id'] == mod_id), None)
    if mod is None:
        raise Http404('Mod not found')
    return render(request, 'main/mod_detail.html', {'mod': mod})


def search(request):
    query = request.GET.get('q', '').strip()
    results = []
    if query:
        q = query.lower()
        for mod in MODS:
            haystack = ' '.join([
                mod['name'],
                mod['description'],
                mod['slug'],
                mod['category'],
            ]).lower()
            if q in haystack:
                results.append(mod)
    return render(request, 'main/search.html', {'query': query, 'mods': results})


def register(request):
    return render(request, 'main/register.html')


def register_submit(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST only'}, status=405)
    try:
        data = json.loads(request.body)
    except (ValueError, TypeError):
        return JsonResponse({'error': 'invalid json'}, status=400)
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    print(f'[register] username={username!r}, email={email!r}, password={password!r}')
    return JsonResponse({'message': 'ok', 'username': username, 'email': email})
