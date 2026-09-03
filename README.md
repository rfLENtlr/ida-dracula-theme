# Dracula Theme for IDA

English | [日本語](README.ja.md)

A Dracula Classic theme for IDA Pro, IDA Home, and IDA Free 9.x, designed for
the current IDA 9.4 release. It covers IDA's UI chrome as well as the
disassembly listing, pseudocode, function graph, debugger, navigation band,
hex view, diff views, and embedded source editors.

The project deliberately ships a native `theme.css`, not an IDAPython plugin.
IDA has loaded themes natively since 7.3, and current theme-manager plugins
ultimately install the same file under the user's `themes` directory. Importing
IDA's built-in `dark` theme also preserves version-specific rules and icons for
new widgets such as Pathfinder and the redesigned Xrefs Graph.

## Compatibility

- Target: IDA 9.x, including the current IDA 9.4 line
- Theme syntax and every IDA-specific property are validated against IDA 9.1
- IDA 8.x may work, but it is not a supported target
- IDA 7.2 and older `.clr` themes are not supported

IDA 9.2 moved its plugin UI stack to Qt 6. This theme contains no Python or
compiled Qt dependency, so it does not need a Qt-version-specific plugin build.

## Install

### Script (recommended)

Linux or macOS:

```sh
./install.sh
```

Windows PowerShell:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\install.ps1
```

Both scripts install to the standard IDA user directory. Override it when your
configuration lives elsewhere:

```sh
IDA_USER_DIR="/path/to/ida/user/dir" ./install.sh
```

```powershell
.\install.ps1 -IdaUserDir 'C:\path\to\ida-user-dir'
```

The scripts also honor `IDAUSR` when it names a single directory.

### Zip or manual install

Extract [`dist/dracula-ida-theme.zip`](dist/dracula-ida-theme.zip) into your
IDA user `themes` directory so the final path is:

```text
<IDA user directory>/themes/dracula/theme.css
```

Default user directories:

- Linux and macOS: `~/.idapro`
- Windows: `%APPDATA%\Hex-Rays\IDA Pro`

Restart IDA, open `Options` → `Colors…`, and select `dracula` as the current
theme. If Windows 11 renders list selections too subtly, select the `Fusion`
Qt style in the same dialog, as recommended by the IDA documentation.

## Uninstall

Linux or macOS:

```sh
./install.sh --uninstall
```

Windows PowerShell:

```powershell
.\install.ps1 -Uninstall
```

Uninstall removes only the distributed `theme.css`. IDA's optional
`themes/dracula/user.css` overrides are deliberately preserved.

## Palette

The semantic mapping follows the Dracula specification and the companion
Ghidra port:

| Role | Color |
| --- | --- |
| Background | `#282A36` |
| Current line / selection | `#44475A` |
| Foreground | `#F8F8F2` |
| Comments | `#6272A4` |
| Types / registers | `#8BE9FD` |
| Functions / code references | `#50FA7B` |
| Parameters / alternate operands | `#FFB86C` |
| Keywords / instructions | `#FF79C6` |
| Constants / numbers | `#BD93F9` |
| Errors / invalid targets | `#FF5555` |
| Strings / character literals | `#F1FA8C` |

Marker, breakpoint, graph-node, and diff backgrounds use opaque blends of the
same palette so light text remains readable.

## Development

Validate the source and optionally compare all IDA-specific properties with an
installed IDA release:

```sh
python3 tools/validate_theme.py
python3 tools/validate_theme.py --ida-dir /path/to/ida
```

Build the distribution archive:

```sh
./tools/build-theme-zip.sh
```

See [docs/research.md](docs/research.md) for the compatibility research and
implementation choices.

## Credits

- Palette and syntax semantics: [Dracula specification](https://spec.draculatheme.com/)
- IDA theme system: [Hex-Rays CSS-based styling documentation](https://docs.hex-rays.com/user-guide/configuration/css-based-styling)
- Companion palette source: [Dracula Theme for Ghidra](https://github.com/rfLENtlr/ghidra-dracula-theme)

This is a community port and is not an official Dracula project. See
[LICENSE](LICENSE) and [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
