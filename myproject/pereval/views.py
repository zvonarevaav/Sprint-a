from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .database import DatabaseHandler  # Импортируем наш новый класс
import json


@csrf_exempt
def submit_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            db_handler = DatabaseHandler()

            # Вставка данных пользователя
            user_id = db_handler.insert_user(
                email=data['email'],
                name=data['name'],
                phone=data.get('phone')
            )

            # Вставка данных координат
            coord_id = db_handler.insert_coords(
                latitude=data['latitude'],
                longitude=data['longitude'],
                height=data['height']
            )

            # Вставка данных перевала
            pereval_id = db_handler.insert_pereval(
                user_id=user_id,
                beautyTitle=data['beautyTitle'],
                title=data['title'],
                other_titles=data.get('other_titles'),
                connect=data.get('connect'),
                add_time=data['add_time'],
                coord_id=coord_id,
                winter_level=data.get('winter_level'),
                summer_level=data.get('summer_level'),
                autumn_level=data.get('autumn_level'),
                spring_level=data.get('spring_level')
            )

            # Вставка изображений перевала
            if 'images' in data:
                for image_url in data['images']:
                    db_handler.insert_image(pereval_id, image_url)

            return JsonResponse({"status": "success", "message": "Data submitted successfully", "id": pereval_id},
                                status=201)

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)
