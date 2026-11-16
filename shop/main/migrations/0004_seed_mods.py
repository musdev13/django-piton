from django.db import migrations


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
        'category': 'Performance',
        'mc_version': '1.20+',
        'downloads': '50M+',
        'features': [
            'Переписаний рушій рендерингу на основі OpenGL',
            'Суттєвий приріст FPS на слабких ПК',
            'Сумісність з більшістю популярних шейдерів',
        ],
        'tags': ['Performance', 'Optimization', 'Rendering', 'OpenGL'],
    },
    {
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
        'tags': ['Technology', 'Automation', 'Steampunk', 'Kinetics'],
    },
    {
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
        'tags': ['Shaders', 'Rendering', 'Graphics', 'Optimization'],
    },
]


def seed(apps, schema_editor):
    Tag = apps.get_model('main', 'Tag')
    Mod = apps.get_model('main', 'Mod')

    tag_cache = {}
    for name in {t for m in MODS for t in m['tags']}:
        slug = name.lower().replace(' ', '-')
        tag_cache[name], _ = Tag.objects.get_or_create(
            name=name, defaults={'slug': slug}
        )

    for data in MODS:
        data = {**data}
        tag_names = data.pop('tags')
        mod, _ = Mod.objects.update_or_create(slug=data['slug'], defaults=data)
        mod.tags.set([tag_cache[n] for n in tag_names])


def unseed(apps, schema_editor):
    Mod = apps.get_model('main', 'Mod')
    Tag = apps.get_model('main', 'Tag')
    Mod.objects.filter(slug__in=[m['slug'] for m in MODS]).delete()
    Tag.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_tag_mod'),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
