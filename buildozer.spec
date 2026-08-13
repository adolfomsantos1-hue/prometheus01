[app]

title = Prometheus 01
package.name = prometheus01
package.domain = org.prometheus

source.dir = .
source.include_exts = py

version = 1.0.0

requirements = python3

orientation = portrait

fullscreen = 0

android.api = 33
android.minapi = 24
android.ndk = 25b
android.sdk = 33
android.archs = arm64-v8a

android.permissions = INTERNET,ACCESS_NETWORK_STATE,ACCESS_WIFI_STATE

android.manifest.extra = <uses-permission android:name="android.permission.INTERNET"/>

[buildozer]

log_level = 2

warn_on_root = 1
