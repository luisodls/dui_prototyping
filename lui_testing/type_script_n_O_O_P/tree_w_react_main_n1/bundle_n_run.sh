echo "removing bundled dist file"
rm -r dist
echo "translating ts 2 js and bundling"
npx webpack
echo "running"
echo " "
firefox index.html
echo " "
echo "removing bundled dist file"
rm -r dist
echo  "... Done"


