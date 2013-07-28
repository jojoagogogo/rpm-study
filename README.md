rpm-study
================


1.必要なライブラリ入れていきます
================
***yum install rpm-build make gcc autoconf automake***

2.作業ディレクトリをつくります
================

通常 ~/rpmbuild ですが

rpmの環境変数で変更可能です

rpm --showrc で現在有効な変数が見れます
**rpm --showrc|grep _topdir**



マクロの設定を変更できるファイル
```
       /usr/lib/rpm/macros
       /etc/rpm/macros.*
       ~/.rpmmacros
```

cat ~/.rpmmacros 
%_topdir /tmp/rpmbuild

***mkdir -p ~/rpmbuild/{BUILD,BUILDROOT,RPMS,SOURCES,SPECS,SRPMS}***

3.SPECファイルの作成
================
SPECSフォルダにspecファイルを置きます

***vi ~/rpmbuild/SPECS/hello.spec***

```
Name:           hello
Version:        1.0.0
Release:        1%{?dist}
Summary:        GaiaX RPM Hacks test code
Group:          Gaiax Test
License:        GPL License
URL:            https://github.com/jojoagogogo/
Source0:        %{name}-%{version}.tar.gz
#Patch0:         %{name}.patch0
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
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc
%{prefix}/hello


%changelog

```


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

***mkdir -p ~/source/hello-1.0.0***

***vi ~/source/hello-1.0.0/hello.c***


```
#include <stdio.h>;

int main(void)
{
    printf("hello, world!\n");  
    return 0;
}
```


***vi ~/source/hello-1.0.0/Makefile***

```

CC      =     gcc
DEST    =     /usr/local/bin
PROGRAM =     hello


${PROGRAM}:   hello.c
(tabにしてください)gcc -o hello hello.c


install:      ${PROGRAM}
(tabにしてください)install -s ${PROGRAM} ${DEST}

clean:
(tabにしてください)rm -f m.o *~ ${PROGRAM}

```


固めます

***cd ~/source***

***tar zcfp ~/rpmbuild/SOURCES/hello-1.0.0.tar.gz hello-1.0.0***



5.ディレクトリの確認
================
```
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
```


6.rpmbuildコマンド実行
==================
***rpmbuild -ba ~/rpmbuild/SPECS/hello.spec***

rpmbuildオプションの説明↓↓↓

```
-ba  バイナリパッケージとソースパッケージの作成
-bp  ソースの展開とパッチ当てまで
-bc  makeまで
-bi  インストールまで
-bb  バイナリパッケージの作成
-bs  ソースパッケージの作成
```


7.結果は・・・・・・・・
==================
```
├── rpmbuild
│   ├── BUILD
│   │   └── hello-1.0.0
│   │       ├── Makefile
│   │       ├── hello
│   │       └── hello.c
│   ├── BUILDROOT
│   ├── RPMS
│   │   └── x86_64
│   │       └── hello-1.0.0-1.el6.x86_64.rpm
│   ├── SOURCES
│   │   └── hello-1.0.0.tar.gz
│   ├── SPECS
│   │   └── hello.spec
│   └── SRPMS
│       └── hello-1.0.0-1.el6.src.rpm
└── source
    └── hello-1.0.0
        ├── Makefile
        └── hello.c
```


8.Patchの作成、配置
================
せっかくなんでパッチをつくります

***cd ~/source/hello-1.0.0/***

***sed s/world/RPM/g hello.c > hello_a.c***

***diff -rNc hello.c hello_a.c > ~/source/hello.patch0***

***cat ~/source/hello.patch0***

```
*** hello.c     2013-07-26 20:10:48.340124666 +0900
--- hello_a.c   2013-07-28 11:50:39.961138071 +0900
***************
*** 2,8 ****
  
  int main(void)
  {
!     printf("hello, world!\n");  
      return 0;
  }
  
--- 2,8 ----
  
  int main(void)
  {
!     printf("hello, RPM!\n");  
      return 0;
  }
  
```

patchをコピー

***cp ~/source/hello.patch0 ~/rpmbuild/SOURCES***


9.SPECの修正
================
パッチを適用するように修正
```
Release:        2%{?dist}

Patch0:         %{name}.patch0

%patch0 -p0
```

10.rpmをつくりなおしてみよう
```
├── rpmbuild
│   ├── BUILD
│   │   └── hello-1.0.0
│   │       ├── Makefile
│   │       ├── hello
│   │       └── hello.c
│   ├── BUILDROOT
│   ├── RPMS
│   │   └── x86_64
│   │       ├── hello-1.0.0-1.el6.x86_64.rpm
│   │       └── hello-1.0.0-2.el6.x86_64.rpm
│   ├── SOURCES
│   │   ├── hello-1.0.0.tar.gz
│   │   └── hello.patch0
│   ├── SPECS
│   │   └── hello.spec
│   └── SRPMS
│       ├── hello-1.0.0-1.el6.src.rpm
│       └── hello-1.0.0-2.el6.src.rpm
└── source
    ├── hello-1.0.0
    │   ├── Makefile
    │   ├── hello.c
    │   └── hello_a.c
    └── hello.patch0


```

***rpmbuild -ba ~/rpmbuild/SPECS/hello.spec***





<!--
1. new spec file

    #rpmdev-newspec %{PROGRAM NAME}
-->

