from typer.testing import CliRunner

from raglab_techdocs.cli import app


runner = CliRunner()


def test_info_command():
    result = runner.invoke(app, ["info"])

    assert result.exit_code == 0
    assert "raglab" in result.output.lower()


def test_help_command():
    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "Usage" in result.output or "usage" in result.output