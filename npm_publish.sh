#!/bin/bash
# npm publish script for sen-dev-patterns skill
# Usage: npm_publish.sh

set -e

echo "=== Publishing sen-dev-patterns to npm ==="

# 检查npm版本
npm --version

# 登录到npm (如果未登录)
echo "Please login to npm if not already:"
echo "  npm login"
echo ""

# 发布到npm
echo "Publishing to npm..."
npm publish --access public

echo ""
echo "=== Done ==="
echo "npm package published: https://www.npmjs.com/package/sen-dev-patterns"
