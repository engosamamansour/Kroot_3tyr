[app]
title = VodafoneFakka
package.name = vodafonefakka
package.domain = org.fakka
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy,requests
orientation = portrait
fullscreen = 0
android.permissions = INTERNET,ACCESS_NETWORK_STATE
android.api = 31
android.minsdk = 21
android.archs = arm64-v8a

[buildozer]
log_level = 1
warn_on_root = 1
