from datetime import datetime
from pydantic import BaseModel, ConfigDict

class EducationalMaterialBase(BaseModel):
    title: str
    description: str
    publication_date: datetime
    file_url: str
    file_type: str
    category_id: int
    user_id: int
    education_level: str

    model_config = ConfigDict(from_attributes=True)

class EducationalMaterialCreate(EducationalMaterialBase):
    publication_date: datetime | None = None

class EducationalMaterialResponse(EducationalMaterialBase):
    id_material: int
