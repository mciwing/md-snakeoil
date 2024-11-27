from pathlib import Path
from textwrap import dedent

import pytest

from md_snakeoil import Formatter


@pytest.fixture
def example_markdown():
    return Path("tests/test.md").read_text()


def test_read_markdown(example_markdown):
    formatter = Formatter()
    content = formatter.read_markdown("tests/test.md")
    assert content == example_markdown


def test_format_single_block():
    formatter = Formatter()
    code = "x = [1,2,344,    3]"
    formatted = formatter.format_single_block(code)
    assert formatted == "x = [1, 2, 344, 3]"


def test_format_markdown_content(example_markdown):
    formatter = Formatter()
    formatted_content = formatter.format_markdown_content(
        file_name="test.md", content=example_markdown
    )

    # check if the formatted content has the expected changes
    assert "x = [1, 2, 344, 3]" in formatted_content

    # check if imports were sorted
    assert (
        "from pathlib import Path\n\nfrom sklearn import datasets"
        in formatted_content
    )
    # previously, the dict spanned multiple lines
    assert '{"a": 1, "b": 2, "f": 323}' in formatted_content


def test_run_inplace(tmp_path, example_markdown):
    formatter = Formatter()
    test_file = tmp_path / "copy.md"
    test_file.write_text(example_markdown)

    formatter.run(test_file, inplace=True)

    # check if the file was updated in-place
    assert test_file.read_text() != example_markdown


def test_run_output_file(tmp_path, example_markdown):
    formatter = Formatter()
    test_file = tmp_path / "copy.md"
    test_file.write_text(example_markdown)

    output_file = tmp_path / "formatted_index.md"
    formatter.run(test_file, output_path=output_file)

    # check if the output file was created with the expected content
    assert output_file.exists()
    assert output_file.read_text() != example_markdown
    assert "x = [1, 2, 344, 3]" in output_file.read_text()


def test_different_indentation_levels():
    markdown_content = Path("tests/indentation.md").read_text()

    formatter = Formatter()
    formatted = formatter.format_markdown_content(
        file_name="", content=dedent(markdown_content)
    )

    assert "    ```python\n    x = [1, 2, 3]\n    ```" in formatted
    assert "        ```python\n        y = [4, 5, 6]\n        ```" in formatted


def test_different_info_strings():
    markdown_content = Path("tests/info_strings.md").read_text()
    formatter = Formatter()
    formatted = formatter.format_markdown_content(
        file_name="", content=dedent(markdown_content)
    )
    assert "```python\nx = [1, 2, 3]\n```" in formatted
    assert "```py\ny = [4, 5, 6]\n```" in formatted
    assert "```Python\nz = [7, 8, 9]\n```" in formatted
    assert "```python startline=3 $%@#$\na = [10, 11, 12]\n```" in formatted