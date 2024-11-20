echo "Welcome to AUTO GIT! 🚀 Embrace the power of automation!\n"
git status

git add .
echo "✅ Files have been successfully staged for commit.\n"

echo "Enter Your commit message..."
read COMMIT_MESSAGE

echo "Enter the mode (fix, feat)..."
read MODE

if [ "$MODE" = "feat" ]; then
    PREFIX="feat:"
elif [ "$MODE" = "update" ]; then
    PREFIX="update:"
elif [ "$MODE" = "fix" ]; then
    PREFIX="fix:"
else
    echo "Invalid mode entered. Please use 'fix', 'update' or 'feat'."
    exit 1
fi

FINAL_COMMIT_MESSAGE="${PREFIX}${COMMIT_MESSAGE}"
git commit -m "$FINAL_COMMIT_MESSAGE"

echo "Enter branch name"
read BRANCH_NAME

git push origin $BRANCH_NAME

echo "Do you want to make a PR (yes, no)"
read DECISION

if [ "$DECISION" = "yes" ]; then
    gh pr create --base main --head $BRANCH_NAME --title "$COMMIT_MESSAGE"
    echo "Pull request opened successfully."
elif [ "$DECISION" = "no" ]; then
    echo "Your changes have been pushed."
else
    echo "Invalid input. Please enter 'yes' or 'no'."
    exit 1
fi
