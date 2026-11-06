from django.http import HttpResponse
from django.shortcuts import render

MODS = [
    {
        'slug': 'sodium',
        'name': 'Sodium',
        'logo': 'main/img/sodium-logo.webp',
        'description': (
            'Оптимізаційний мод, що переписує рушій рендерингу Minecraft: '
            'суттєво підвищує FPS, зменшує мікрозатримки та споживання пам\'яті '
            'без втрати якості зображення.'
        ),
    },
    {
        'slug': 'create',
        'name': 'Create',
        'logo': 'main/img/create-logo.webp',
        'description': (
            'Технічний мод про обертові механізми, шестерні, конвеєри та складну '
            'автоматизацію з впізнаваним естетичним стилем у дусі стімпанку.'
        ),
    },
    {
        'slug': 'iris',
        'name': 'Iris Shaders',
        'logo': 'main/img/iris-logo.webp',
        'description': (
            'Легкий та швидкий завантажувач шейдерів із підтримкою пакетів для '
            'OptiFine та повною сумісністю з Sodium — красива гра без просідань FPS.'
        ),
    },
]


def main(request):
    return render(request, 'main/index.html', {'mods': MODS})


def about(request):
    return render(request, 'main/about.html')
