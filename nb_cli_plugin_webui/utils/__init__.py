import re
import random
import socket
import string
from typing import Any, List

from ..i18n import _
from ..exceptions import TokenComplexityError


def find_available_port(start_port: int, end_port: int) -> int:
    for port in range(start_port, end_port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.bind(("localhost", port))
            return port
        except socket.error:
            pass
        finally:
            sock.close()

    raise ValueError(_("No available ports in this range."))


def check_token_complexity(token: str) -> None:
    if len(token) < 12:
        raise TokenComplexityError(_("Token should be at least 12 characters long."))

    if not re.search(r"\d", token):
        raise TokenComplexityError(_("Token should contain at least one digit."))
    if not re.search(r"[a-z]", token):
        raise TokenComplexityError(
            _("Token should contain at least one lowercase letter.")
        )
    if not re.search(r"[A-Z]", token):
        raise TokenComplexityError(
            _("Token should contain at least one uppercase letter.")
        )
    if not re.search(r"[ !@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]", token):
        raise TokenComplexityError(
            _("Token should contain at least one special character.")
        )


def generate_complexity_string(
    length: int = random.randint(12, 18),
    *,
    use_digits: bool = False,
    use_punctuation: bool = False
) -> str:
    return str().join(
        random.choices(
            string.ascii_letters
            + (string.digits if use_digits else str())
            + (string.punctuation if use_punctuation else str()),
            k=length,
        )
    )


def filling_str(text: str, target_length: int) -> str:
    return text + str().join([" " for _ in range(0, target_length - len(text))])


def decode_parse(data: bytes) -> str:
    encodings = ["utf-8", "gbk"]
    decoded_data = str(data)
    for encoding in encodings:
        try:
            decoded_data = data.decode(encoding)
        except UnicodeDecodeError:
            continue
    return decoded_data


def safe_list_get(_list: List[Any], _index: int, default: Any) -> Any:
    try:
        return _list[_index]
    except IndexError:
        return default
