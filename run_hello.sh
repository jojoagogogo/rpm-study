
VER=1.0.0
cp -Rfv source/hello ./hello-${VER}
tar zcvfp rpmbuild/SOURCES/hello-${VER}.tar.gz hello-${VER}
rm -Rf hello-${VER}

rpmbuild -ba rpmbuild/SPECS/hello.spec

