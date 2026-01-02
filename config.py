import os

# Possible values:
# "LOCAL"  -> real POS (printing enabled)
# "CLOUD"  -> demo mode (printing disabled)
APP_MODE = os.getenv("APP_MODE", "LOCAL")
