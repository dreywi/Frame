"""Вспомогательные функции безопасного ввода."""

from typing import Optional


def input_int(prompt: str, min_value: Optional[int] = None,
              max_value: Optional[int] = None) -> int:
    """Запрашивать целое число, пока не будет введено корректное."""
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
        except ValueError:
            print("Введите целое число")
            continue
        if min_value is not None and value < min_value:
            print(f"Число должно быть не меньше {min_value}")
            continue
        if max_value is not None and value > max_value:
            print(f"Число должно быть не больше {max_value}")
            continue
        return value


def input_text(prompt: str) -> str:
    """Запрашивать непустую строку."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Значение не может быть пустым")
