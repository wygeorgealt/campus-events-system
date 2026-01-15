
import os
import sys
import django
from django.core.management import call_command

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "example.settings")
django.setup()

try:
    call_command('migrate')
except Exception as e:
    print(f"ERROR TYPE: {type(e)}")
    print(f"ERROR MESSAGE: {str(e)}")
    import traceback
    traceback.print_exc()
    if hasattr(e, '__cause__') and e.__cause__:
        print(f"CAUSED BY: {type(e.__cause__)}")
        print(f"CAUSE MESSAGE: {str(e.__cause__)}")
