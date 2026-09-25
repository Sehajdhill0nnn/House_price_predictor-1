from typing import Literal

from pydantic import BaseModel, Field, field_validator


class HouseFeatures(BaseModel):
    overall_qual: int = Field(ge=1, le=10)
    gr_liv_area: float = Field(gt=0, le=100000)
    garage_cars: float = Field(ge=0, le=10)
    garage_area: float = Field(ge=0, le=10000)
    total_bsmt_sf: float = Field(ge=0, le=100000)
    first_flr_sf: float = Field(gt=0, le=100000)
    second_flr_sf: float = Field(ge=0, le=100000)
    full_bath: float = Field(ge=0, le=10)
    bedroom_abv_gr: int = Field(ge=0, le=20)
    tot_rms_abv_grd: int = Field(ge=1, le=30)
    year_built: int = Field(ge=1800, le=2026)
    year_remod_add: int = Field(ge=1800, le=2026)
    lot_area: float = Field(gt=0, le=1000000)
    neighborhood: str = Field(min_length=1, max_length=30)
    kitchen_qual: Literal["Ex", "Gd", "TA", "Fa", "Po"]
    exter_qual: Literal["Ex", "Gd", "TA", "Fa", "Po"]
    bsmt_qual: Literal["Ex", "Gd", "TA", "Fa", "Po", "None"]
    garage_type: Literal["Attchd", "Detchd", "BuiltIn", "CarPort", "Basment", "2Types", "None"]
    heating: Literal["GasA", "GasW", "Grav", "Wall", "OthW", "Floor"]
    central_air: Literal["Y", "N"]

    @field_validator("year_remod_add")
    @classmethod
    def remodeled_after_built(cls, value: int, info):
        built = info.data.get("year_built")
        if built is not None and value < built:
            raise ValueError("year_remod_add must be greater than or equal to year_built")
        return value
