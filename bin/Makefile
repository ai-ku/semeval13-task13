all: scripts fastsubs dists runpca.m runiso.m readsparse.mexa64 runsc.m wkmeans

scripts: check
	test -e $@ || ln -s ../src/scripts/* .

fastsubs: check
	#test -e ../src/fastsubs || (cd ../src/ ; git clone ${FASTSUBS_GIT_REPO} ; git checkout ${FASTSUBS_GIT_TAG}) 
	cd ../src/fastsubs; make
	test -e $@ || ln -s ../src/fastsubs/fastsubs .
	test -e subs || ln -s ../src/fastsubs/subs .
	test -e wordsub || ln -s ../src/fastsubs/wordsub .

dists: check
	#test -e ../src/dists || (cd ../src/ ; git clone ${DIST_GIT_REPO} ; git checkout ${DIST_GIT_TAG}) 
	cd ../src/dist; make
	test -e $@ || ln -s ../src/dist/dists .

runsc.m: check
	cd ../src/spectral;
	test -e $@ || ln -s ../src/spectral/runsc.m
	test -e sc.m || ln -s ../src/spectral/sc.m

runpca.m: check
	cd ../src/pca;
	test -e $@ || ln -s ../src/pca/runpca.m

runlle.m: check
	cd ../src/lle;
	test -e $@ || ln -s ../src/lle/runlle.m
	test -e lle.m || ln -s ../src/lle/lle.m

runiso.m: check
	cd ../src/iso; make
	test -e $@ || ln -s ../src/iso/runiso.m
	test -e IsomapII.m || ln -s ../src/iso/IsomapII.m
	test -e dijkstra.mexa64 || ln -s ../src/iso/dijkstra.mexa64
	test -e dfun.m || ln -s ../src/iso/dfun.m
	test -e L2_distance.m || ln -s ../src/iso/L2_distance.m

readsparse.mexa64: check
	test -e $@ || ln -s ../src/readsparse.mexa64

scode: check
	#test -e ../src/scode || (cd ../src/ ; git clone ${SCODE_GIT_REPO} ; git checkout ${SCODE_GIT_TAG}) 
	cd ../src/scode; make
	test -e $@ || ln -s ../src/scode/scode .

wkmeans: check
	#test -e ../src/wkmeans || (cd ../src/ ; git clone ${WKMEANS_GIT_REPO} ; git checkout ${WKMEANS_GIT_TAG}) 
	cd ../src/wkmeans; make
	test -e $@ || ln -s ../src/wkmeans/wkmeans .

check:
	true

clean:
	-rm *.m *.pl *.pyc *.py *.gp *.sh fastsubs subs dists scode wkmeans wordsub *.mexa64 *~
