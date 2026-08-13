[app]
title = VodafoneFakka
package.name = vodafonefakka
package.domain = org.fakka
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy==2.3.0,requests,certifi,openssl
orientation = portrait
fullscreen = 0
android.permissions = INTERNET,ACCESS_NETWORK_STATE
android.api = 33
android.minsdk = 21
android.archs = arm64-v8a
android.accept_sdk_license = True

[buildozer]
log_level = 1
warn_on_root = 1
