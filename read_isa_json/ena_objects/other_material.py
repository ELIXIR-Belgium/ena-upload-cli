from ena_objects.ena_std_lib import validate_dict
from ena_objects.parameter_value import ParameterValue
from ena_objects.other_material_characteristic import OtherMaterialCharacteristic
from ena_objects.characteristic import IsaBase

from typing import List, Dict


class OtherMaterial(IsaBase):
    """
    docstring
    """

    mandatory_keys = ["id", "name", "type", "other_material_characteristics"]

    def __init__(
        self,
        id: int,
        name: str,
        type: str,
        other_material_characteristics: OtherMaterialCharacteristic,
    ) -> None:
        self.id = id
        self.name = name
        self.type = type
        self.other_material_characteristics = other_material_characteristics

    def from_dict(self, dict):
        super().check_dict_keys(dict, self.mandatory_keys)
        return OtherMaterial(
            id=dict["id"],
            name=dict["name"],
            type=dict["type"],
            other_material_characteristics=OtherMaterialCharacteristic.from_dict(
                dict["other_material_characteristics"]
            ),
        )
