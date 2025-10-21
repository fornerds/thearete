"""Database models package."""

# Import all models here to ensure they are registered with SQLAlchemy
from app.db.models.customer import Customer  # noqa: F401
from app.db.models.item import Item  # noqa: F401
from app.db.models.photo import Photo  # noqa: F401
from app.db.models.shop import Shop  # noqa: F401
from app.db.models.skin_color_measurement import SkinColorMeasurement  # noqa: F401
from app.db.models.token import UserToken  # noqa: F401
from app.db.models.treatment import Treatment  # noqa: F401
from app.db.models.treatment_session import TreatmentSession  # noqa: F401
from app.db.models.user import User  # noqa: F401

__all__ = ['Customer', 'Item', 'Photo', 'Shop', 'SkinColorMeasurement', 'Treatment', 'TreatmentSession', 'User', 'UserToken']
