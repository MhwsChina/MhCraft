# MhCraft
[contributors-shield]: https://img.shields.io/github/contributors/MhwsChina/MhCraft.svg?style=flat-square
[contributors-url]: https://github.com/MhwsChina/MhCraft/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/MhwsChina/MhCraft.svg?style=flat-square
[forks-url]: https://github.com/MhwsChina/MhCraft/network/members
[stars-shield]: https://img.shields.io/github/stars/MhwsChina/MhCraft.svg?style=flat-square
[stars-url]: https://github.com/MhwsChina/MhCraft/stargazers
[issues-shield]: https://img.shields.io/github/issues/MhwsChina/MhCraft.svg?style=flat-square
[issues-url]: https://github.com/MhwsChina/MhCraft/issues
[license-shield]: https://img.shields.io/github/license/MhwsChina/MhCraft.svg?style=flat-square
[license-url]: https://github.com/MhwsChina/MhCraft/blob/master/LICENSE
[![Stargazers][stars-shield]][stars-url]
[![Forks][forks-shield]][forks-url]
[![Issues][issues-shield]][issues-url]
[![Contributors][contributors-shield]][contributors-url]
[![GPL-3 License][license-shield]][license-url]
</br>
这是一个mc启动器(使用python编写)</br>
感谢使用,有什么bug欢迎提出</br>
该项目为MhLauncher的重新编写版,功能会陆续加回去</br>
下载源代码后运行mhcraft.py可以使用</br>
[[点击前往蓝奏云下载]](https://wwbxb.lanzouw.com/b00yb7zrij)密码:2026
# MHCraft 自动化构建与发布系统

本项目配置了完整的 GitHub Actions 自动化流水线。当针对 `main` 分支发布新的 Release 时，系统会自动在 Linux、Windows 和 macOS 平台上构建可执行文件，并将其同步到 Release 附件中。

## 🚀 自动化工作流说明

本项目包含两个核心工作流文件：

### 1. `check.yml` (检测与同步)
- **触发时机**：当在 GitHub 上正式发布（Publish）一个指向 `main` 分支的 Release 时触发。
- **核心职责**：
  - 校验 Release 的目标分支是否为 `main`。
  - 调用 `buildpy.yml` 执行多平台构建。
  - 构建完成后，自动下载所有平台的构建产物（Artifact），并作为附件上传到当前 Release 页面。

### 2. `buildpy.yml` (多平台构建)
- **触发时机**：仅被 `check.yml` 调用（`workflow_call`）。
- **构建环境**：使用 Python 3.14（支持预发布版本）。
- **构建逻辑**：
  - 在 `ubuntu-latest`、`windows-latest` 和 `macos-latest` 上并行运行。
  - 自动安装 `requirements.txt` 中的依赖。
  - 使用 PyInstaller 进行打包，默认参数包含：
    - `--clean`：自动清理临时文件，确保构建环境纯净。
    - `-w`：隐藏控制台窗口（适用于 GUI 程序）。
    - `-i favicon.ico`：使用项目根目录下的 `favicon.ico` 作为程序图标。
    - `--onefile`：打包为单一可执行文件。

## 🛠️ 如何触发自动构建？

1. 进入 GitHub 仓库，点击右侧的 **Releases**。
2. 点击 **Draft a new release**。
3. 确保 **Target** 分支选择的是 `main`。
4. 填写版本号（Tag）和发布标题。
5. 点击底部的 **Publish release**（注意：必须是 Publish，Save as draft 不会触发）。
6. 前往 **Actions** 页面，即可实时查看构建进度。构建完成后，刷新 Release 页面即可看到三个平台的压缩包附件。

## 📂 本地开发注意事项

- 项目根目录已配置 `.gitignore`，构建产生的 `dist/`、`build/`、`*.spec` 等文件会被自动忽略。
- 确保 `favicon.ico` 和 `mhcraft.py` 位于同一目录下，否则 PyInstaller 打包时会因找不到图标而报错。
