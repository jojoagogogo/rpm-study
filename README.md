rpm-study
=========

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





<!--
1. new spec file

    #rpmdev-newspec %{PROGRAM NAME}
-->

