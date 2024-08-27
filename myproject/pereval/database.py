from .models import User, Coords, Pereval, PerevalImage


class DatabaseHandler:

    def insert_user(self, email, name, phone):
        """
        Вставляет нового пользователя или получает существующего по email.
        """
        user, created = User.objects.get_or_create(email=email, defaults={'name': name, 'phone': phone})
        return user.id

    def insert_coords(self, latitude, longitude, height):
        """
        Вставляет новые координаты в базу данных.
        """
        coords = Coords.objects.create(latitude=latitude, longitude=longitude, height=height)
        return coords.id

    def insert_pereval(self, user_id, beautyTitle, title, other_titles, connect, add_time, coord_id, winter_level,
                       summer_level, autumn_level, spring_level):
        """
        Вставляет новую запись о перевале.
        """
        pereval = Pereval.objects.create(
            user_id=user_id,
            beautyTitle=beautyTitle,
            title=title,
            other_titles=other_titles,
            connect=connect,
            add_time=add_time,
            coord_id=coord_id,
            winter_level=winter_level,
            summer_level=summer_level,
            autumn_level=autumn_level,
            spring_level=spring_level,
            status='new'  # Устанавливаем статус как "new" при создании
        )
        return pereval.id

    def insert_image(self, pereval_id, image_url):
        """
        Вставляет новое изображение для перевала.
        """
        image = PerevalImage.objects.create(pereval_id=pereval_id, image_url=image_url)
        return image.id
