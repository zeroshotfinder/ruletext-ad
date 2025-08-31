from pydantic import BaseModel, Field, computed_field, model_serializer
from typing import List, Optional
from typing import Literal, Annotated
from enum import Enum
from collections import Counter

class BreakFastBoxModel(BaseModel):
    name: Literal["almonds", "bananas", "tangerine", "nectarine", "cereals", "package", "other"]  = Field(..., description="The object name")
    size: Literal["small", "medium", "large"] = Field(..., description="The size of the object")
    location: Literal["top", "middle", "bottom"] = Field(..., description="The location of the object")
    direction: Literal["left", "center", "right"] = Field(..., description="The direction of the object in the image")

class JuiceBottleFirstLabelModel(BaseModel):
    fruit: Literal["banana", "orange", "cherry"] = Field(None, description="Fruit depicted on the label")
    location: Literal["top", "middle", "bottom"] = Field(..., description="The location of the object in relation to the juice bottle")
    direction: Literal["left", "center", "right"] = Field(..., description="The direction of the object in the image in relation to the juice bottle")

class JuiceBottleSecondLabelModel(BaseModel):
    phrase: Literal["100 % Juice"] = Field(None, description="Phrase written on the label")
    location: Literal["top", "middle", "bottom"] = Field(..., description="The location of the object in relation to the juice bottle")
    direction: Literal["left", "center", "right"] = Field(..., description="The direction of the object in the image in relation to the juice bottle")

class VolumeEnum(str, Enum):
    EMPTY = "empty"
    HALF_FULL = "half full"
    ALMOST_FULL = "almost full"
    FULL = "full"  # use 'full', no 'full to the brim'

class JuiceBottleModel(BaseModel):
    name: Literal["juice bottle"]  = Field(None, description="The object name")
    juice_color: Literal["white", "yellow", "red"] = Field(None, description="The color of the juice")
    first_label: Optional[JuiceBottleFirstLabelModel] = Field(None, description="First label on the bottle")
    second_label: Optional[JuiceBottleSecondLabelModel] = Field(None, description="The second label on the bottle")
    
    volume: VolumeEnum = Field(
        ...,
        description="Volume of the juice in the bottle: empty, half full, almost full, or full."
    )
    juice_color_label_content_pair: Annotated[
        str,
        Field(
            description=(
                "Combination of juice_color and first_label.fruit, "
                "formatted as 'color,fruit'; ex: 'white,banana'"
            )
        )
    ]

class SplicingConnectorsCableModel(BaseModel):
    name: Literal["cable"] = Field(None, description="The object name")
    color: Literal["blue", "yellow", "red"] = Field(None, description="The color of the object")
    measurement: Literal["very short", "short", "medium", "long"] = Field(None, description="The mesure of the object")
    damage: Literal["no", "yes"] = Field(None, description="if the cable is damaged")
    amount: int = Field(..., ge=0, description="The amount of cable")

class SplicingConnectorsConnectorModel(BaseModel):
    name: Literal["connector"] = Field(None, description="The object name")
    color: Literal["red", "orange"] = Field(None, description="The color of the object")
    number_of_keys: Literal["2 keys", "3 keys", "5 keys"] = Field(None, description="The number of keys of the connector")
    amount: int = Field(..., description="The amount of connector")

class SplicingConnectorsModel(BaseModel):
    name: Literal["splicing connectors"] = Field(None, description="The object name")
    cables: List[SplicingConnectorsCableModel] = Field(None, description="The cable of the splicing connectors")
    connectors: List[SplicingConnectorsConnectorModel] = Field(None, description="The connector of the splicing connectors")
    
    keys_and_cable_color_pair: Annotated[
        str,
        Field(
            description=(
                "Combination of connector.number_of_keys and cable.color, "
                "formatted as 'connector_key,cable_color'; ex: '2 keys,yellow'"
            )
        )
    ]
    
class CellOfCaseModel(BaseModel):
    name: Literal["cell_of_case"] = Field(..., description="The object name")
    has_more_than_one_pusphin_per_cell: Literal["no", "yes"] = Field(...,description="if are there more than one pushpin in cell")

class PushipinModel(BaseModel):
    name: Literal["pushpin"] = Field(None, description="The object name")
    cells_of_case: List[CellOfCaseModel] = Field(None, description="The cells of the case")
    total_amount_of_pushpins: int = Field(..., ge=0, description="The total amount of pushpins in the case")

class ScrewBagModel(BaseModel):    
    has_two_bolts: Literal["no", "yes"] = Field(..., description="If there are  two bolts in the bag")
    has_two_nuts: Literal["no", "yes"] = Field(..., description="If there are two nuts in the bag")
    has_two_washers: Literal["no", "yes"] = Field(..., description="If there are  two washers in the bag")

class ObjectModelTest(BaseModel):
    name: Literal["almonds", "bananas", "tangerine", "nectarine", "cereals", "package"]  = Field(..., description="The object name")
    size: Literal["small", "medium", "large"] = Field(..., description="The size of the object")
    location: Literal["top", "middle", "bottom"] = Field(..., description="The location of the object")
    direction: Literal["left", "center", "right"] = Field(..., description="The direction of the object in the image")
    color: Literal["white", "orange", "yellow", "red", "brown", "beige"] = Field(..., description="The main color of the object")
    amount: int = Field(..., ge=0, description="The amount of the object")
    description: str = Field(..., description="The full description of the object")

class ObjectRuleModel(BaseModel):
    name: Literal["almonds", "bananas", "tangerine", "nectarine", "cereals", "package"] = Field(..., description="The object name")
    sizes: List[Literal["small", "medium", "large"]] = Field(..., description="Possible size of the object")
    locations: List[Literal["top", "middle", "bottom"]] = Field(..., description="Possible locations of the object")
    directions: List[Literal["left", "center", "right"]] = Field(..., description="Possible directions of the object in the image")
    colors: List[str] = Field(..., description="Possible colors of the object")
    amount: int = Field(..., ge=0, description="The amount of the object")

class AnomalyResponse(BaseModel):
    has_anomaly: bool
    description: str = Field(..., description="Description of the anomaly")

class AnalysisResponse(BaseModel):
    has_anomaly: bool =  Field(..., description="If the test image description have an anomaly")
    description: str = Field(..., description="Description of the analysis")

class CheckListModel(BaseModel):
    anomalies_checklist: List[BreakFastBoxModel]