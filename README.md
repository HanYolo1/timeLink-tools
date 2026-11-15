# timeLink build tools

The build tools [`tools.lock`](https://github.com/HanYolo1/timeLink/blob/main/tools.lock) names, as assets of this
repository's [`tools` release](https://github.com/HanYolo1/timeLink-tools/releases/tag/tools).

timeLink is built on your PC from your own copy of the game. Its builder needs a compiler, a Python, an emsdk, FFmpeg,
SDL2, a glibc sysroot and a few prebuilt DLLs. Those are large binaries, so they are not in the timeLink repository:
`tools.lock` names them by URL, and this repository is where they live.

## What is here, and what is not

**Third-party binaries and prebuilt files only.** llvm-mingw, Python, emsdk, FFmpeg, SDL2, a glibc 2.35 sysroot, the CPM
cache, wgpu-native, and the prebuilt DLLs of `third_party` (`a64emit.dll`, `lld-link.exe`, `SDL2.dll`, `SDL3.dll`,
`zbic.dll`).

**No game data.** No ROM, no dump, no `.nup`, no `romfs` or `exefs`, nothing derived from one. This repository exists so
that a build tool can be downloaded without an account; it holds nothing that belongs to the game or to a player.

## How an asset is named

```
<sha256>-<name>.zip
```

The digest is the archive's own SHA-256, which `tools.lock` records and every consumer checks. A replaced asset is
therefore caught. **Never reuse a version string**: a new archive is a new asset name.

## How they are made

`scripts/rehost_tools.py` in the timeLink repository stages them: it downloads each archive from the first URL
`tools.lock` names, checks it against the recorded SHA-256 and size, and writes it here under its asset name.
`scripts/tools.py mirror` uploads a new one when a tool is bumped.

## Licences

Each archive carries its own. llvm-mingw is Apache-2.0 with LLVM exceptions; Python is the PSF licence; emsdk is LLVM's;
FFmpeg is LGPL-2.1-or-later; SDL2 is zlib; the glibc sysroot is LGPL-2.1-or-later; wgpu-native is Apache-2.0/MIT. The
licence texts travel inside the archives.
