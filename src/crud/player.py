from django.db import transaction
from datetime import date

from core.models.player_django import Player, Level, PlayerLevel, LevelPrize


def assign_prize_for_level_completion(player_id, level_id):
    """
    Присваивает игроку приз за прохождение уровня
    """
    try:
        with transaction.atomic():
            # Находим игрока и уровень
            player = Player.objects.get(player_id=player_id)
            level = Level.objects.get(id=level_id)

            # Обновляем или создаем запись о прохождении уровня
            player_level, created = PlayerLevel.objects.get_or_create(
                player=player,
                level=level,
                defaults={'is_completed': True, 'completed': date.today()}
            )

            if not created and not player_level.is_completed:
                player_level.is_completed = True
                player_level.completed = date.today()
                player_level.save()

            # Находим все призы для этого уровня и отмечаем как полученные
            level_prizes = LevelPrize.objects.filter(level=level)
            for level_prize in level_prizes:
                level_prize.received = date.today()
                level_prize.save()

            return True, "Призы успешно присвоены"

    except Player.DoesNotExist:
        return False, "Игрок не найден"
    except Level.DoesNotExist:
        return False, "Уровень не найден"
    except Exception as e:
        return False, f"Ошибка: {str(e)}"