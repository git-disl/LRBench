conda activate $1

export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
export PYTHONPATH=$PYTHONPATH:`pwd`
export DJANGO_SETTINGS_MODULE=LRBenchDjango.settings

# avoid committing the settings.py
# git update-index --assume-unchanged  LRBenchDjango/settings.py
