#!/bin/bash

if git tag | grep -q "$NEW_VERSION"; then
    echo "Tag $NEW_VERSION already exists. Delete it ..."
    git tag -d $NEW_VERSION
fi 
