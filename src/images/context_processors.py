from images import models


def inappropriate_counter(request):
    return {
        "inappropriate_counter": models.Image.objects.filter(inappropriate=True).count()
    }
