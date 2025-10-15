import os
def get_thread_count():
    """Calculate optimal threads based on hardware."""
    return os.cpu_count() // 2 + 1  # Heuristic for balance
