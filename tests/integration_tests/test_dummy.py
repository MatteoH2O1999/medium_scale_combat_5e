import subprocess


def test_dummy(executable_path):
    completed_process = subprocess.run(executable_path, capture_output=True)
    assert completed_process.returncode == 0
