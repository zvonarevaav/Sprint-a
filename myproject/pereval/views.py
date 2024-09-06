from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Pereval, User, Coords, PerevalImage

@csrf_exempt
def submit_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            # Вставка данных пользователя
            user, _ = User.objects.get_or_create(
                email=data['user']['email'],
                defaults={
                    'name': data['user']['name'],
                    'phone': data['user']['phone']
                }
            )

            # Вставка данных координат
            coord = Coords.objects.create(
                latitude=data['coords']['latitude'],
                longitude=data['coords']['longitude'],
                height=data['coords']['height']
            )

            # Вставка данных перевала
            pereval = Pereval.objects.create(
                user=user,
                beautyTitle=data['beautyTitle'],
                title=data['title'],
                other_titles=data.get('other_titles'),
                connect=data.get('connect'),
                add_time=data['add_time'],
                coord=coord,
                winter_level=data['level'].get('winter'),
                summer_level=data['level'].get('summer'),
                autumn_level=data['level'].get('autumn'),
                spring_level=data['level'].get('spring'),
            )

            # Вставка изображений перевала
            if 'images' in data:
                for image_data in data['images']:
                    PerevalImage.objects.create(
                        pereval=pereval,
                        image_url=image_data['image']
                    )

            return JsonResponse({
                "status": "success",
                "message": "Data submitted successfully",
                "id": pereval.id  # Возвращаем ID перевала
            }, status=201)

        except KeyError as e:
            return JsonResponse({"status": "error", "message": f"Missing required field: {str(e)}"}, status=400)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)


# Новый метод для получения записи по id
def get_pereval(request, id):
    try:
        pereval = Pereval.objects.get(id=id)
        data = {
            "id": pereval.id,
            "beautyTitle": pereval.beautyTitle,
            "title": pereval.title,
            "other_titles": pereval.other_titles,
            "connect": pereval.connect,
            "add_time": pereval.add_time,
            "status": pereval.status,
            "user": {
                "email": pereval.user.email,
                "name": pereval.user.name,
                "phone": pereval.user.phone
            },
            "coords": {
                "latitude": pereval.coord.latitude,
                "longitude": pereval.coord.longitude,
                "height": pereval.coord.height
            },
            "level": {
                "winter": pereval.winter_level,
                "summer": pereval.summer_level,
                "autumn": pereval.autumn_level,
                "spring": pereval.spring_level
            },
            "images": [image.image_url for image in pereval.images.all()]  # Исправлено на pereval.images.all()
        }
        return JsonResponse(data, status=200)
    except Pereval.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Pereval not found"}, status=404)


@csrf_exempt
def update_pereval(request, id):
    if request.method == 'PATCH':
        try:
            pereval = Pereval.objects.get(id=id)
            if pereval.status != 'new':
                return JsonResponse({"state": 0, "message": "Cannot edit, status is not 'new'"}, status=400)

            data = json.loads(request.body)

            # Обновление полей перевала, за исключением данных пользователя
            pereval.beautyTitle = data.get('beautyTitle', pereval.beautyTitle)
            pereval.title = data.get('title', pereval.title)
            pereval.other_titles = data.get('other_titles', pereval.other_titles)
            pereval.connect = data.get('connect', pereval.connect)
            pereval.coord.latitude = data.get('latitude', pereval.coord.latitude)
            pereval.coord.longitude = data.get('longitude', pereval.coord.longitude)
            pereval.coord.height = data.get('height', pereval.coord.height)
            pereval.winter_level = data.get('winter_level', pereval.winter_level)
            pereval.summer_level = data.get('summer_level', pereval.summer_level)
            pereval.autumn_level = data.get('autumn_level', pereval.autumn_level)
            pereval.spring_level = data.get('spring_level', pereval.spring_level)

            # Сохраняем обновленные координаты и перевал
            pereval.coord.save()
            pereval.save()

            # Возвращаем только состояние успешного обновления
            return JsonResponse({"state": 1, "message": "Pereval updated successfully"}, status=200)

        except Pereval.DoesNotExist:
            return JsonResponse({"state": 0, "message": "Pereval not found"}, status=404)
        except Exception as e:
            return JsonResponse({"state": 0, "message": str(e)}, status=500)

    return JsonResponse({"state": 0, "message": "Invalid request"}, status=400)


# Новый метод для получения всех перевалов пользователя по email
def get_perevals_by_user(request):
    email = request.GET.get('user__email')
    if email:
        user = User.objects.filter(email=email).first()
        if user:
            perevals = Pereval.objects.filter(user=user)
            data = [
                {
                    "id": pereval.id,
                    "beautyTitle": pereval.beautyTitle,
                    "title": pereval.title,
                    "status": pereval.status
                }
                for pereval in perevals
            ]
            return JsonResponse(data, status=200, safe=False)
        return JsonResponse({"status": "error", "message": "User not found"}, status=404)
    return JsonResponse({"status": "error", "message": "Email not provided"}, status=400)
