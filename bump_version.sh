#!/bin/bash

# The path to your setup.py
SETUP_FILE="setup.py"

# Extract the current version from setup.py
CURRENT_VERSION=$(grep -Po "(?<=version=\")[^\"]+" $SETUP_FILE)

# Break the version number into an array using '.' as delimiter
IFS='.' read -r -a version_parts <<< "$CURRENT_VERSION"

# Increment the patch number
((version_parts[2]++))

# Reassemble the version number
NEW_VERSION="${version_parts[0]}.${version_parts[1]}.${version_parts[2]}"

# Replace the old version number with the new one in setup.py
sed -i "s/version=\"$CURRENT_VERSION\"/version=\"$NEW_VERSION\"/" $SETUP_FILE

# Output the new version
echo "Updated setup.py with new version: $NEW_VERSION"

