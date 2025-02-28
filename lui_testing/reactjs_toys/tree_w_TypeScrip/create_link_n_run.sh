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
echo "remember reproduce the following answers"
echo ""
echo " Would you like to use TypeScript? … Yes                                 <= Yes  "
echo " Would you like to use ESLint? … No                                      <= No   "
echo " Would you like to use Tailwind CSS? … No                                <= No   "
echo " Would you like your code inside a 'src/' directory? … Yes               <= Yes  "
echo " Would you like to use App Router? (recommended) … No                    <= No   "
echo " Would you like to use Turbopack for 'next dev'? … No                    <= No   "
echo " Would you like to customize the import alias ('@/*' by default)? … No   <= No   "
echo ""

npx create-next-app@latest tst-app

echo "changing directory to tst-app/src/pages/"
cd tst-app/src/pages/

echo "replacing index.js with link to my code"
mv index.tsx original_index.tsx
ln $INI_DIR/control_tree.tsx index.tsx
cd ../../

echo "running my code"
echo "npm run dev"
npm run dev
