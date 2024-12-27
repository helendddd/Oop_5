import io
import pathlib
from unittest.mock import MagicMock, patch

from src.individual import display_tree


# Тесты для pytest
def test_display_tree_with_files(mocker):
    # Создаем фиктивную директорию с файлом
    fake_file = MagicMock()
    fake_file.is_dir.return_value = False
    fake_file.is_file.return_value = True
    fake_file.name = "file.txt"
    fake_file.stat.return_value.st_size = 1234

    mocker.patch("pathlib.Path.iterdir", return_value=[fake_file])

    # Патчим вывод
    with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
        display_tree(
            pathlib.Path("/test_dir"),
            MagicMock(s=None, a=False, f=False, d=False, t=False),
            "",
        )
        output = mock_stdout.getvalue().strip()

    # Используем assert для проверки, что в выводе есть нужная информация
    assert (
        "└── file.txt (1234 bytes)" in output
    ), f"Expected '└── file.txt (1234 bytes)' in output, but got {output}"


def test_display_tree_hidden_files(mocker):
    # Создаем фиктивную директорию с скрытым файлом
    fake_file = MagicMock()
    fake_file.is_dir.return_value = False
    fake_file.is_file.return_value = True
    fake_file.name = ".hidden_file"
    fake_file.stat.return_value.st_size = 1234

    mocker.patch("pathlib.Path.iterdir", return_value=[fake_file])

    # Патчим вывод с флагом -a для отображения скрытых файлов
    with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
        display_tree(
            pathlib.Path("/test_dir"),
            MagicMock(s=None, a=True, f=True, d=False, t=False),
            "",
        )
        output = mock_stdout.getvalue().strip()

    # Проверка, что скрытый файл отображается
    assert (
        ".hidden_file (1234 bytes)" in output
    ), f"Expected '.hidden_file (1234 bytes)' in output, but got {output}"
