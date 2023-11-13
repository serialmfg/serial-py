#!/bin/bash

NEW_VERSION=$1

# Check if the tag exists locally
if git tag | grep -q "$NEW_VERSION"; then
    echo "Tag $NEW_VERSION already exists locally. Deleting it..."
    git tag -d $NEW_VERSION 
fi 

# Check if the tag exists in the remote repository
if git ls-remote --tags origin | grep -q "refs/tags/$NEW_VERSION"; then
    echo "Tag $NEW_VERSION also exists in the remote repository. Deleting it..."
    git push --delete origin $NEW_VERSION
fi

