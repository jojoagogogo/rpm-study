rpm-study
================


1.必要なライブラリ入れていきます
================
yum install rpm-build make gcc autoconf automake 

2.作業ディレクトリをつくります
================

<pre>
通常 ~/rpmbuild ですが

rpmの環境変数で変更可能です

rpm --showrc で現在有効な変数が見れます
rpm --showrc|grep _topdir
</pre>
<pre>
マクロの設定を変更できるファイル
       /usr/lib/rpm/macros
       /etc/rpm/macros.*
       ~/.rpmmacros
       
cat ~/.rpmmacros 
%_topdir /tmp/rpmbuild
</pre>

mkdir -p ~/rpmbuild/{BUILD,BUILDROOT,RPMS,SOURCES,SPECS,SRPMS}

3.SPECファイルの作成
================
SPECSフォルダにspecファイルを置きます

vi ~/rpmbuild/SPECS/hello.spec 
<pre>
Name:           hello
Version:        1.0.0
Release:        1%{?dist}
Summary:        GaiaX RPM Hacks test code
Group:          Gaiax Test
License:        GPL License
URL:            https://github.com/jojoagogogo/
Source0:        %{name}-%{version}.tar.gz
Patch0:         %{name}.patch0
#BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root 
Vendor:         "GaiaX co.,ltd."

BuildRequires: autoconf automake
Requires:      glibc

Prefix: /usr/local/bin

%description
hello sample spec :)

%prep
%setup -q
#%setup -q -n %{name}
#%patch0 -p0


%build

rm -rf $RPM_BUILD_ROOT
%if %{with configure}
%configure
%endif
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{prefix}
#make install DESTDIR=$RPM_BUILD_ROOT
make install DEST=$RPM_BUILD_ROOT%{prefix}


%clean
#rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc
%{prefix}/hello


%changelog

</pre>

今回使っているSPECの変数です↓↓↓

* spec

**宣言部**  

| 名前 | 意味 | 例 | 必須 |
|:-----------|:------------|:------------------|:------------:|
| Name:  | パッケージ名 | hello | * | 
| Version: | バージョン | 1.0.0 | * | 
| Release: | パッケージのリリース番号| 1%{?dist}  | * |
| Summmary:  | パッケージの内容 | rpm sample | * |
| Group:  | パッケージのグループ yum grouplist 適当でもOK? | rpm sample | * |
| License: | ライセンス | GPL License | |
| URL: |開発ベンダーのURL|http://github/jojoagogogo/||
| Source0: | ソースの入手先|  %{name}-%{version}.tar.gz | * |
| Patch0: |  パッチファイルの指定、複数可  | %{name}.patch0 |    |
| BuildRequires: | ビルド時の依存 | autoconf automake gcc|    |
| Reauires: | インストール時の依存 | glibc |    |
| %description | パッケージの詳細 |    |    |
| %changelog   |変更履歴|    |    |

**実行部**  

| 名前 | 意味 | 例 | 必須 |
|:-----------|:------------|:------------------|:------------:|
|%prep|パッケージ作成前に行う作業|| * |
|%setup|ソースファイルを展開、移動|%setup -q -n %{name}-%{version}| * |
|%patch0|パッチの適用|%patch0 -p0|  |
|%build|ビルド実行|configure makeを行う| | * |
|%configure|configure|||
|%install|make installを行う|make install| * |
|%clean|ゴミを削除|rm $RPM_BUILD_ROOT| * |
|%files|インストールするファイルを記述|%{prefix}/hello||


4.ソースファイルの作成
================
tarballで固めたMakefile hello.cをつくります

mkdir -p ~/source/hello-1.0.0

vi source/hello-1.0.0/hello.c 
<pre>
#include &lt;stdio.h&gt;

int main(void)
{
    printf("hello, world!\n");  
    return 0;
}
</pre>

vi source/hello-1.0.0/Makefile
<pre>
CC      =     gcc
DEST    =     /usr/local/bin
PROGRAM =     hello


${PROGRAM}:   hello.c
(tabにしてください)gcc -o hello hello.c


install:      ${PROGRAM}
(tabにしてください)install -s ${PROGRAM} ${DEST}

clean:
(tabにしてください)rm -f m.o *~ ${PROGRAM}
</pre>


固めます

cd ~/source

tar zcfp ~/rpmbuild/SOURCES/hello-1.0.0.tar.gz hello-1.0.0



5.ディレクトリの確認
================
<pre>
.
├── BUILD
├── BUILDROOT
├── RPMS
├── SOURCES
│   ├── hello-1.0.0.tar.gz
│   └── hello.patch0
├── SPECS
│   └── hello.spec
└── SRPMS
</pre>


6.rpmbuildコマンド実行
==================
rpmbuild -ba ~/rpmbuild/SPECS/hello.spec

rpmbuildコマンドの説明↓↓↓

7.結果は・・・・・・・・
==================



8.Patchの作成、配置
================
せっかくなんでパッチをつくります



cp ~/source/hello.patch0 ~/rpmbuild/SOURCES







<!--
1. new spec file

    #rpmdev-newspec %{PROGRAM NAME}
-->

