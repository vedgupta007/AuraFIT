import pytest
from pydantic import BaseModel, Field, ValidationError

class HeightModel(BaseModel):
    height_cm: float = Field(..., gt=0, lt=300)

def test_valid_centimeters():
    model = HeightModel(height_cm=173)
    assert model.height_cm == 173

def test_invalid_negative_centimeters():
    with pytest.raises(ValidationError):
        HeightModel(height_cm=-5)

def test_invalid_zero_centimeters():
    with pytest.raises(ValidationError):
        HeightModel(height_cm=0)

def test_unreasonably_large_centimeters():
    with pytest.raises(ValidationError):
        HeightModel(height_cm=400)
