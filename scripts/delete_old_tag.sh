#!/bin/bash

NEW_VERSION=$1
PAT=$2

# Check if the tag exists locally
if git tag | grep -q "$NEW_VERSION"; then
    echo "Tag $NEW_VERSION already exists locally. Deleting it..."
    git tag -d $NEW_VERSION 
fi 


