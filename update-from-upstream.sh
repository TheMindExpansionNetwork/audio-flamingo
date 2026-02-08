#!/bin/bash
# Update from upstream repository

echo "🔄 Fetching upstream changes..."
git fetch upstream

echo "📊 Checking for updates..."
git log --oneline HEAD..upstream/main --decorate 2>/dev/null || echo "No new commits"

echo ""
read -p "Merge upstream changes? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    git checkout main
    git merge upstream/main
    git push origin main
    echo "✅ Updated and pushed!"
else
    echo "❌ Update cancelled"
fi
