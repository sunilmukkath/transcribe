#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DIST="${ROOT}/dist"
APP_NAME="ET-Scribe"
APP_BUNDLE="${DIST}/${APP_NAME}.app"
PY_DIST="${DIST}/${APP_NAME}"

if [[ ! -d "${PY_DIST}" ]]; then
  echo "Missing ${PY_DIST}. Run pyinstaller first:"
  echo "  cd ${ROOT} && pyinstaller --noconfirm packaging/et_scribe.spec"
  exit 1
fi

rm -rf "${APP_BUNDLE}"
mkdir -p "${APP_BUNDLE}/Contents/MacOS"
mkdir -p "${APP_BUNDLE}/Contents/Resources"

# One-folder layout: executable + _internal live together inside MacOS
cp -R "${PY_DIST}/"* "${APP_BUNDLE}/Contents/MacOS/"

EXEC_NAME="${APP_NAME}"
chmod +x "${APP_BUNDLE}/Contents/MacOS/${EXEC_NAME}"

cat > "${APP_BUNDLE}/Contents/Info.plist" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>CFBundleExecutable</key>
  <string>${EXEC_NAME}</string>
  <key>CFBundleIdentifier</key>
  <string>com.elastictree.etscribe</string>
  <key>CFBundleName</key>
  <string>${APP_NAME}</string>
  <key>CFBundlePackageType</key>
  <string>APPL</string>
  <key>CFBundleShortVersionString</key>
  <string>1.0</string>
  <key>CFBundleVersion</key>
  <string>1</string>
  <key>LSMinimumSystemVersion</key>
  <string>11.0</string>
</dict>
</plist>
EOF

DMG="${DIST}/${APP_NAME}.dmg"
rm -f "${DMG}"
hdiutil create -volname "${APP_NAME}" -srcfolder "${APP_BUNDLE}" -ov -format UDZO "${DMG}"

echo "Built: ${DMG}"
