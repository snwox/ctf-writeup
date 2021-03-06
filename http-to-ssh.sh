#/bin/bash
#-- Script to automate https://help.github.com/articles/why-is-git-always-asking-for-my-password

REPO_URL="https://github.com/snwox/ctf-writeup"
if [ -z "$REPO_URL" ]; then
  echo "-- ERROR:  Could not identify Repo url."
  echo "   It is possible this repo is already using SSH instead of HTTPS."
  exit
fi

USER="snwox"
if [ -z "$USER" ]; then
  echo "-- ERROR:  Could not identify User."
  exit
fi

REPO="ctf-writeup"
if [ -z "$REPO" ]; then
  echo "-- ERROR:  Could not identify Repo."
  exit
fi

NEW_URL="git@github.com:$USER/$REPO.git"
echo "Changing repo url from "
echo "  '$REPO_URL'"
echo "      to "
echo "  '$NEW_URL'"
echo ""

CHANGE_CMD="git remote set-url origin $NEW_URL"
`$CHANGE_CMD`

echo "Success"
