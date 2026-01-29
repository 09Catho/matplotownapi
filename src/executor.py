import matplotlib
matplotlib.use('Agg')  # For headless servers
import matplotlib.pyplot as plt
import numpy as np
import io
import traceback

def execute_plot_code(code: str) -> io.BytesIO:
    """
    Executes the provided Python code in a restricted environment
    and returns a BytesIO buffer containing the PNG image.

    Raises Exception if code execution fails.
    """
    # Setup a fresh plot context
    plt.close('all')
    buf = io.BytesIO()

    # Allow only safe builtins (very basic sandboxing)
    # Note: exec is dangerous. In a real production env, use better isolation.
    # We allow builtins so imports work, but this is not secure.
    safe_globals = {"plt": plt, "np": np}

    try:
        exec(code, safe_globals)
        plt.savefig(buf, format='png', bbox_inches='tight', dpi=200)
        plt.close()
        buf.seek(0)
        return buf
    except Exception:
        plt.close()
        raise
