import os
import pkgutil
from importlib import import_module

base_dir = os.path.dirname(__file__)
print(base_dir)
implementor_map = {}
for loader, implementor, ispkg in pkgutil.iter_modules([base_dir]):
    print(loader, implementor, ispkg)
    try:
        module = import_module(f"{os.path.basename(base_dir)}.{implementor}")
        task_implementor = getattr(module, "TaskImplementor")
        implementor_map[implementor] = task_implementor
    except Exception as e:
        pass
print(implementor_map)