---
title: Android Studio配置Gradle
date: 2025-4-20 23:00:00
tags:
 - Gradle
 - Android
 - 入门实践
---



在**IntelliJ IDEA** 和**Android Studio** 中，可以通过以下步骤指定 Gradle 主目录（Gradle Home Directory）。这个设置允许你使用手动安装的 Gradle 版本，而不是依赖 IDE 自动下载的版本。

<!--more-->

------

### **步骤 1：打开设置窗口**

1. 启动 IntelliJ IDEA 或 Android Studio。
2. 打开 **设置/首选项** 窗口：
   - **Windows/Linux** 作系统 ：`File > Settings`。
   - **macOS** ：`IntelliJ IDEA > Preferences`。

------

### **步骤 2：导航到 Gradle 设置**

1. 在设置窗口中，展开左侧的**Build, Execution, Deployment** 菜单
2. 点击**Build Tools > Gradle** 。

------

### **步骤 3：指定 Gradle 主目录**

在右侧的 Gradle 设置面板中，找到**“Gradle JVM”** 和**“Use Gradle from”** 部分

##### **选项 1：使用 Gradle Wrapper**

- 默认情况下，IDE 会选择**'gradle-wrapper.properties' 文件**。
- 这意味着 IDE 会根据项目中的`gradle/wrapper/gradle-wrapper.properties`文件自动下载并使用指定的 Gradle 版本。
- 如果你希望继续使用 Wrapper 方式，则无需更改此设置。

##### **选项 2：手动指定 Gradle 主目录**

如果需要手动指定 Gradle 主目录，请按照以下步骤作：

1. 将**“Distribution”** 下**指定位置** 。
2. 点击右侧的文件夹图标（或直接输入路径），选择你手动安装的 Gradle 目录。
   - 例如：
     - Windows：`C:\Gradle\gradle-8.11.1`
     - macOS/Linux：`/opt/gradle/gradle-8.11.1`
   - 确保该目录包含以下子目录和文件：
     - `bin/gradle`（可执行文件）
     - `lib/gradle`

------

### **步骤 4：配置 Gradle JVM**

1. 在同一设置页面，找到 **Gradle JVM** 部分。
2. 选择一个合适的 JDK 版本用于运行 Gradle。
   - 如果未列出所需的 JDK，可以点击右侧的下拉菜单，选择**添加 JDK** 并

------

### **步骤 5：应用更改**

1. 点击**Apply** 或 **OK** 按钮保存设置。
2. 如果项目已经打开，IDE 可能会提示重新加载 Gradle 配置。点击**Reload** 或 **Sync Now**以应用更改。

------

### **步骤 6：验证设置是否生效**

1. 打开终端（Terminal）窗口，运行以下命令检查 Gradle 版本：

   ```bash
   gradle --version
   ```

   输出应显示你指定的 Gradle 版本。

2. 在 IDE 中，尝试构建项目，确保 Gradle 构建成功。

------

### **额外注意事项**

1. **兼容性检查** ：

   - 确保指定的 Gradle 版本与项目的`build.gradle`文件兼容。

   - 如果项目需要特定的 Gradle 版本，请参考`gradle-wrapper.properties`文件中的`distributionUrl`。

   - 示例 `gradle-wrapper.properties`文件内容：

     ```bash
     distributionUrl=https\://services.gradle.org/distributions/gradle-8.11.1-bin.zip
     ```

2. **环境变量** ：

   - 如果你在系统中设置了`GRADLE_HOME`环境变量，IDE 通常会自动检测到它，但仍需在设置中明确指定路径

3. **代理设置** 

   如果你的网络需要代理，确保在 IDE 的 HTTP Proxy 设置中正确配置代理信息：

   - 路径：`File > Settings > Appearance & Behavior > System Settings > HTTP Proxy`

------

通过以上步骤，你可以成功在 IntelliJ IDEA 或 Android Studio 中指定 Gradle 主目录，并使用手动安装的 Gradle 版本进行项目构建。如果有其他问题，请随时补充说明！

