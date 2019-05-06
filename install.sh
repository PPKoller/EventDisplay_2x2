#ParaView Installation File

mkdir ParaView
mkdir ParaView/ParaView-5.4.1
mkdir ParaView/Source

#wget 'https://mega.nz/#!gQADUKIR!hZagPcd6aJR0f6Tw7nbObShPTgz2s39MrZlyvoVdnZs' -P ParaView/Source

tar -xzvf ParaView/Source/ParaView-5.4.1*.gz --strip 1 -C ParaView/ParaView-5.4.1

echo "# ParaView Setup File" > setup.sh

installPath=$(pwd)
echo "installPath='$installPath'" >> setup.sh

paraviewPath="${installPath}/ParaView/ParaView-5.4.1"
echo "paraviewPath='$paraviewPath'" >> setup.sh

echo "export LD_LIBRARY_PATH="\${LD_LIBRARY_PATH}:\${paraviewPath}/lib/paraview-5.4"" >> setup.sh
echo "export PYTHONPATH="\${PYTHONPATH}:\${paraviewPath}/lib/python2.7/site-packages"" >> setup.sh

source setup.sh

