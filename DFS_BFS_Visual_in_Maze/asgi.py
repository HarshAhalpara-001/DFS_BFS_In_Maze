"""
ASGI config for DFS_BFS_Visual_in_Maze project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DFS_BFS_Visual_in_Maze.settings')

application = get_asgi_application()
