# IDA theme research and design notes

Checked on 2026-09-03.

## Findings

1. **IDA 9.4 is the current release.** Hex-Rays announced the final release on
   2026-07-13. It adds Pathfinder, a redesigned Xrefs Graph, a unified Scripts
   window, and other UI surfaces. Hex-Rays also specifically notes dark-theme
   improvements for tree expand/collapse arrows.
2. **A color theme does not need to be an IDAPython plugin.** IDA discovers
   `<IDAUSR>/themes/<name>/theme.css` and exposes the directory name under
   `Options` → `Colors…`. Hex-Rays recommends the user directory because it is
   writable and survives installation of a newer IDA version.
3. **Extending a built-in theme is the forward-compatible pattern.** Hex-Rays'
   current example uses `@importtheme` and a small set of overrides. Extending
   `dark` keeps its platform workarounds, current internal widget selectors,
   and bundled dark icons.
4. **Current theme plugins are installers and authoring tools.** IDA Theme
   Explorer 1.0.3 (IDA >= 9.0) downloads `theme.css` and assets into IDA's user
   `themes` directory. `ida-themr` 0.1.0 adds inspection and VS Code conversion,
   but its output is still a native theme directory.
5. **The older Dracula/IDA theme is not a sufficient 9.x reference.** Its
   stylesheet still uses several historical widget names such as `TChooser`,
   `MainMsgList`, and `TextEdit`, and imports `_base` directly. IDA 9.1's own
   theme uses `chooser_widget_t`, `log_widget_t`, and `text_area_t`. This port
   uses the current names while retaining only harmless compatibility selectors
   where they also cover diff or output widgets.

## Resulting architecture

```text
IDA's built-in dark theme (version-specific rules and icons)
                         |
                         v
              dracula/theme.css
        +----------------+----------------+
        |                |                |
        v                v                v
  Qt UI chrome    analysis widgets   source/debug views
```

The package contains no executable plugin code and makes no network requests.
Its install scripts copy one file into the user's IDA directory. This avoids
PySide/Qt 5-versus-Qt 6 coupling while allowing each installed IDA release to
supply its own newest base rules.

## Semantic mapping

The canonical Dracula mapping is preserved where IDA exposes a corresponding
token:

- instructions and keywords → Pink
- functions and code references → Green
- types, registers, and data references → Cyan
- parameters and alternate operands → Orange
- numeric constants → Purple
- strings and character constants → Yellow
- errors and invalid references → Red
- comments and non-primary metadata → Comment blue

IDA often expects opaque colors for graph nodes, debugger rows, highlights,
and diff regions. Those use the same dark blends as the companion Ghidra port
instead of placing bright canonical colors directly behind foreground text.

## Sources

- [IDA 9.4 release](https://hex-rays.com/blog/ida-9.4-release-a-new-dyld-shared-cache-swift-analysis-new-teams-add-on-and-more-)
- [IDA 9.4 navigation and dark-theme improvements](https://hex-rays.com/blog/ida-9.4-smarter-navigation-and-quality-of-life-improvements)
- [Hex-Rays: CSS-based styling](https://docs.hex-rays.com/user-guide/configuration/css-based-styling)
- [Hex-Rays: Styling IDA listings background with CSS](https://hex-rays.com/blog/ui-candy)
- [IDA Theme Explorer](https://github.com/kevinmuoz/ida-theme-explorer)
- [ida-themr](https://github.com/mahmoudimus/ida-themr)
- [Older Dracula/IDA port](https://github.com/dracula/ida)
- [Dracula syntax highlighting specification](https://spec.draculatheme.com/)
