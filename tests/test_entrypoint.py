import subprocess

import entrypoint


def write_cmake_file(workspace):
    """Create a representative CMake file in the temporary test workspace."""
    cmake_file = workspace / "CMakeLists.txt"
    cmake_file.write_text("set(VAR  1)\n")
    return cmake_file


def run_entrypoint(monkeypatch, workspace, fake_run, cli_args):
    """Run the entrypoint with a patched workspace and mocked cmake-format call."""
    monkeypatch.setenv("GITHUB_WORKSPACE", str(workspace))
    monkeypatch.setattr(entrypoint.subprocess, "run", fake_run)
    return entrypoint.main(cli_args)


def test_check_mode_fails_with_diff(tmp_path, monkeypatch, capsys):
    """Check mode should fail and print a diff when formatting changes are needed."""
    cmake_file = write_cmake_file(tmp_path)

    def fake_run(command, capture_output, text):
        assert command == ['cmake-format', str(cmake_file)]
        return subprocess.CompletedProcess(command, returncode=0, stdout="set(VAR 1)\n", stderr="")

    cli_args = ["--file-regex", "CMakeLists.txt$", "--cmake-format-args", ""]
    exit_code = run_entrypoint(monkeypatch, tmp_path, fake_run, cli_args)
    output = capsys.readouterr().out

    assert exit_code == 1
    assert "Formatting issues found in" in output
    assert "-set(VAR  1)" in output
    assert "+set(VAR 1)" in output


def test_in_place_mode_formats_files(tmp_path, monkeypatch, capsys):
    """In-place mode should report success when cmake-format completes cleanly."""
    cmake_file = write_cmake_file(tmp_path)

    def fake_run(command, capture_output, text):
        assert command == ['cmake-format', '--in-place', str(cmake_file)]
        return subprocess.CompletedProcess(command, returncode=0, stdout="", stderr="")

    cli_args = ["--file-regex", "CMakeLists.txt$", "--cmake-format-args=--in-place"]
    exit_code = run_entrypoint(monkeypatch, tmp_path, fake_run, cli_args)
    output = capsys.readouterr().out

    assert exit_code == 0
    assert f"Successfully formatted {cmake_file}." in output


def test_command_failure_fails_job(tmp_path, monkeypatch, capsys):
    """cmake-format errors should be surfaced and fail the overall job."""
    cmake_file = write_cmake_file(tmp_path)

    def fake_run(command, capture_output, text):
        return subprocess.CompletedProcess(command, returncode=2, stdout="", stderr="invalid config")

    cli_args = ["--file-regex", "CMakeLists.txt$", "--cmake-format-args", ""]
    exit_code = run_entrypoint(monkeypatch, tmp_path, fake_run, cli_args)
    output = capsys.readouterr().out

    assert exit_code == 1
    assert f"Error processing {cmake_file}:" in output
    assert "invalid config" in output
