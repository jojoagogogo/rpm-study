VER=1.0.0

for v in BUILD BUILDROOT RPMS SOURCES SRPMS
do
    rm -Rf rpmbuild/${v}/*
done
cp -Rf source/hello ./hello-${VER}
tar zcfp rpmbuild/SOURCES/hello-${VER}.tar.gz hello-${VER}
cp -Rf source/hello.patch0 rpmbuild/SOURCES
rm -Rf hello-${VER}


rpmbuild -ba rpmbuild/SPECS/hello.spec

# with configure
#rpmbuild -ba rpmbuild/SPECS/hello.spec --with configure

