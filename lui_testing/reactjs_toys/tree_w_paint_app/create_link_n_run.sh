INI_DIR=$(pwd)

echo "changing directory to /tmp"
cd /tmp

echo "removing possible old tst-app directory"
rm -rf tst-app

echo "creating template app with create-next-app@latest"
echo "_________________________________________________"
echo ""
echo "if npm asks ... agree to << create-next-app@XX.X.X >> "
echo ""
echo "then"
echo ""
echo "remember to say << yes >> only to the next question "
echo ""
echo "  Would you like your code inside a '/src' directory?"
echo ""

npx create-next-app@latest tst-app

echo "changing directory to tst-app/src/pages/"
cd tst-app/src/pages/

echo "replacing index.js with link to my code"
mv index.js original_index.js
ln $INI_DIR/tree_w_painter.js index.js
cd ../../

echo "running my code"
echo "npm run dev"
npm run dev




