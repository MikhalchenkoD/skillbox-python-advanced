import subprocess

def process_count(username: str) -> int:
    command = f"ps -u {username} -o pid= | wc -l"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    if process.returncode == 0:
        return int(output.strip())
    else:
        print(f"Error: {error.decode()}")
        return -1

def total_memory_usage(root_pid: int) -> float:
    command = f"ps --ppid {root_pid} -o rss= | awk '{{sum+=$1}} END {{print sum}}'"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    if process.returncode == 0:
        total_memory = int(output.strip())
        return total_memory / (1024 * 1024)
    else:
        print(f"Error: {error.decode()}")
        return -1



