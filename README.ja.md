# Dracula Theme for IDA

[English](README.md) | 日本語

現行のIDA 9.4を中心に設計した、IDA Pro、IDA Home、IDA Free 9.x向けの
Dracula Classicテーマです。通常のUIに加えて、逆アセンブルListing、疑似コード、
Function Graph、Debugger、Navigation Band、Hex View、Diff、内蔵ソース
エディタまで配色します。

このプロジェクトはIDAPythonプラグインではなく、IDAネイティブの`theme.css`を
配布します。IDA 7.3以降はテーマを本体で読み込め、現行のテーマ管理プラグインも
最終的には同じファイルをユーザーの`themes`ディレクトリへ配置しています。また、
IDA組み込みの`dark`テーマを継承することで、新しいIDAで追加されたWidget固有の
規則とアイコンを維持します。

## 対応範囲

- 対象: 現行のIDA 9.4系を含むIDA 9.x
- テーマ構文とIDA固有プロパティはIDA 9.1に対して検証済み
- IDA 8.xでも動作する可能性はありますが、サポート対象外
- IDA 7.2以前の`.clr`形式には非対応

IDA 9.2ではプラグインのUI基盤がQt 6へ移行しました。このテーマはPythonにも
コンパイル済みQtコードにも依存しないため、Qtバージョン別のビルドは不要です。

## インストール

### スクリプト（推奨）

Linux / macOS:

```sh
./install.sh
```

Windows PowerShell:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\install.ps1
```

標準のIDAユーザーディレクトリ以外を使っている場合は、明示できます。

```sh
IDA_USER_DIR="/path/to/ida/user/dir" ./install.sh
```

```powershell
.\install.ps1 -IdaUserDir 'C:\path\to\ida-user-dir'
```

`IDAUSR`が単一ディレクトリを指している場合も自動的に使用します。

### Zipまたは手動インストール

[`dist/dracula-ida-theme.zip`](dist/dracula-ida-theme.zip)をIDAユーザー
ディレクトリ内の`themes`へ展開し、最終的に次の配置にします。

```text
<IDAユーザーディレクトリ>/themes/dracula/theme.css
```

標準のユーザーディレクトリ:

- Linux / macOS: `~/.idapro`
- Windows: `%APPDATA%\Hex-Rays\IDA Pro`

IDAを再起動し、`Options` → `Colors…`のCurrent themeから`dracula`を選択して
ください。Windows 11でリストの選択色が薄く表示される場合は、IDAドキュメントの
推奨どおり、同じダイアログでQt styleを`Fusion`へ変更してください。

## アンインストール

Linux / macOS:

```sh
./install.sh --uninstall
```

Windows PowerShell:

```powershell
.\install.ps1 -Uninstall
```

配布した`theme.css`だけを削除します。IDAが個人設定として作成することのある
`themes/dracula/user.css`は残します。

## 配色

Dracula公式仕様とGhidra版の意味付けをIDAへ対応させています。

| 用途 | 色 |
| --- | --- |
| 背景 | `#282A36` |
| 現在行・選択 | `#44475A` |
| 前景 | `#F8F8F2` |
| コメント | `#6272A4` |
| 型・レジスタ | `#8BE9FD` |
| 関数・コード参照 | `#50FA7B` |
| 引数・代替オペランド | `#FFB86C` |
| キーワード・命令 | `#FF79C6` |
| 定数・数値 | `#BD93F9` |
| エラー・不正な参照 | `#FF5555` |
| 文字列・文字リテラル | `#F1FA8C` |

Marker、Breakpoint、Graph Node、Diffの背景には、明るい文字を読みやすくするため
同じパレットから作った不透明なブレンド色を使用しています。

## 開発・検証

テーマ自体を検証し、必要ならインストール済みIDAのプロパティ一覧とも照合します。

```sh
python3 tools/validate_theme.py
python3 tools/validate_theme.py --ida-dir /path/to/ida
```

配布用zipを再生成します。

```sh
./tools/build-theme-zip.sh
```

現行仕様の調査内容と設計判断は[docs/research.md](docs/research.md)にまとめています。

## クレジット

- 配色とSyntaxの意味付け: [Dracula specification](https://spec.draculatheme.com/)
- IDAテーマ仕様: [Hex-Rays CSS-based styling documentation](https://docs.hex-rays.com/user-guide/configuration/css-based-styling)
- 配色の対応元: [Dracula Theme for Ghidra](https://github.com/rfLENtlr/ghidra-dracula-theme)

これはDracula公式プロジェクトではないコミュニティ移植です。詳細は
[LICENSE](LICENSE)と[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)を参照してください。
