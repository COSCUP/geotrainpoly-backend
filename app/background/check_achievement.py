from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select
from app.database import get_session
from app.models.achievements import Achievement
from app.models.userAchievement import UserAchievement
from app.models.msg import Msg
from app.models.users import User


def check_achievement(user_id: str, relation = None):
    db: Session = next(get_session())
    try:
        user_achievements_select = select(UserAchievement.achievement_id).where(
            UserAchievement.user_id == user_id
        )

        query = db.query(Achievement).filter(
            Achievement.achievement_id.notin_(user_achievements_select)
        )

        if relation is not None:
            query = query.filter(Achievement.achievement_id.in_(relation))

        missing_achievements = query.all()

        user = (db.query(User)
            .filter(User.user_id == user_id)
            .options(joinedload(User.msg))
            .options(joinedload(User.achievements))
            .options(joinedload(User.booths))
            .first()
        )

        for achievement in missing_achievements:
            models = getattr(user, achievement.model)

            if achievement.type == 'LG':
                if len(models) >= int(achievement.goal):
                    db.add(UserAchievement(user_id=user_id, achievement_id=achievement.achievement_id))
                    user.points += achievement.points
            elif achievement.type == 'HAS':
                if achievement.goal in [getattr(m, achievement.column) for m in models]:
                    db.add(UserAchievement(user_id=user_id, achievement_id=achievement.achievement_id))
                    user.points += achievement.points

        db.commit()
    finally:
        db.close()
