echo "removing all << .js >>, << .map >> and << .d. >> files"
rm *.map
rm *.d.*
rm *.js
echo "translating ts 2 js and bundling"
tsc
echo "running"
echo " "
node main1.js
echo " "
echo  "... Done"
echo "removing all << .js >>, << .map >> and << .d. >> files again"
rm *.map
rm *.d.*
rm *.js


