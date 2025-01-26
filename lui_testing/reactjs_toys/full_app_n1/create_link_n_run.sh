INI_DIR=$(pwd)

echo "changing directory to /tmp"
cd /tmp

echo "removing possible old tst-app directory"
rm -rf tst-app

echo "creating template app with create-next-app@latest"
npx create-next-app@latest tst-app

echo "changing directory to tst-app/src/pages/"
cd tst-app/src/pages/

echo "replacing index.js with link to my code"
mv index.js original_index.js
ln $INI_DIR/button_n_request_n_cors_test.js index.js
cd ../../

echo "running my code"
echo "npm run dev"
npm run dev




