from .model import ClassificationModel
from typing import Tuple
from .extract_series_number import extract_serial_number
from .bert import TypeBert


def extract_and_classify(theme: str, description: str) ->Tuple[str, str, str]:
    full_text = theme + " " + description
    type_model = ClassificationModel(
        mode="type"
    )
    type_ = type_model.get_class(full_text)
    stop_dot_model = ClassificationModel(
        mode="stop_dot"
    )
    serial_number_ = extract_serial_number(theme=theme, description=description)
    stop_dot_ = stop_dot_model.get_class(full_text)

    return type_, stop_dot_, serial_number_


def bert_extract_and_classify(theme: str, description: str) ->Tuple[str, str, str]:
    full_text = theme + " " + description
    type_model = TypeBert(
        mode="type"
    )
    type_ = type_model(full_text)
    stop_dot_model = TypeBert(
        mode="stop_dot"
    )
    serial_number_ = extract_serial_number(theme=theme, description=description)
    stop_dot_ = stop_dot_model(full_text)

    return type_, stop_dot_, serial_number_