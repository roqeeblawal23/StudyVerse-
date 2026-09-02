[app]

title = StudyVerse
package.name = studyverse
package.domain = org.studyverse

source.dir = .
source.main = main.py

version = 1.0

requirements = python3==3.13.5,kivy==2.3.1

source.include_exts = py,json,png,jpg,jpeg,kv,atlas

orientation = portrait

android.archs = arm64-v8a
android.api = 33
android.minapi = 24

android.copy_libs = 1
android.accept_sdk_license = True

presplash.filename = %(source.dir)s/presplash.png
icon.filename = %(source.dir)s/icon.png


[buildozer]

log_level = 2
warn_on_root = 0
