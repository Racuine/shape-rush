# Add release signing config to generated Capacitor Android project.
import base64
import os
from pathlib import Path

required = ('KEYSTORE_BASE64', 'KEYSTORE_PASSWORD', 'KEY_ALIAS', 'KEY_PASSWORD')
missing = [k for k in required if not os.environ.get(k)]
if missing:
    raise SystemExit('Missing signing secrets: ' + ', '.join(missing))
app = Path('android/app')
if not app.is_dir():
    raise SystemExit('Run npx cap add android first')
(app / 'shape-rush-upload.jks').write_bytes(base64.b64decode(os.environ['KEYSTORE_BASE64'], validate=True))
# Passwords are passed through environment variables; they are not committed to source control.
gradle = app / 'build.gradle'
s = gradle.read_text()
needle = 'android {'
if needle not in s:
    raise SystemExit('Cannot find android block in generated build.gradle')
block = '''android {
    signingConfigs {
        release {
            storeFile file('shape-rush-upload.jks')
            storePassword System.getenv('KEYSTORE_PASSWORD')
            keyAlias System.getenv('KEY_ALIAS')
            keyPassword System.getenv('KEY_PASSWORD')
        }
    }
'''
s = s.replace(needle, block, 1)
# Capacitor's standard Gradle template includes a release buildType.
needle_release = 'release {'
# The first release { is our signingConfigs release; find buildTypes block first.
idx = s.find('buildTypes {')
if idx < 0:
    raise SystemExit('Cannot find buildTypes in generated build.gradle')
rel = s.find('release {', idx)
if rel < 0:
    raise SystemExit('Cannot find release buildType')
s = s[:rel + len('release {')] + '\n            signingConfig signingConfigs.release' + s[rel + len('release {'):]
gradle.write_text(s)
print('Release signing configured')
