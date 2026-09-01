[app]

# (str) Title of your application
title = StudyVerse

# (str) Package name
package.name = studyverse

# (str) Package domain
package.domain = org.studyverse

# (str) Source code directory
source.dir = .

# (str) Main Python file
source.main = main.py

# (str) Application version
version = 1.0

# (str) Python dependencies
requirements = python3,kivy

# (str) Files to include
source.include_exts = py,json,png,jpg,jpeg,kv,atlas

# (str) Application orientation
orientation = portrait

# (str) Supported Android architecture
android.archs = arm64-v8a

# (int) Android API
android.api = 33

# (int) Minimum Android API
android.minapi = 24

# (str) Android app theme
android.entrypoint = org.kivy.android.PythonActivity

# (bool) Copy libraries
android.copy_libs = 1

# (str) Presplash
presplash.filename = %(source.dir)s/presplash.png

# (str) Icon
icon.filename = %(source.dir)s/icon.png


[buildozer]

# (str) Log level
log_level = 2

# (bool) Warn about running as root
warn_on_root = 0
