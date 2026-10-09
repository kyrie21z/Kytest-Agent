# 执行边界与适用范围

这份说明描述当前实现的执行边界，项目未经过正式安全审计。测试通过不能证明任意恶意输入都安全。

## 默认 Sandbox

命令与测试执行默认使用 Linux Bubblewrap（`sandbox`）。生产执行路径创建独立的网络、PID 等命名空间，移除可提升权限的能力，挂载工作区、只读系统库和当前 Python 安装目录，使用私有临时目录。它不会挂载整个宿主根目录、用户目录或宿主临时目录。

Python 与虚拟环境的安装目录是明确允许的读取范围，不能把它们视为保密存储。工作区同样可被执行中的代码读取；运行不可信任务时，应使用独立工作区，移除其中的凭据与敏感文件。

CLI 的 `-C` 工作区应与 Python 安装和虚拟环境目录分开。不要将虚拟环境装在目标工作区内，或把工作区设为解释器目录；重叠会被拒绝。README 的 `-C examples` 使用独立的源码目录。

文件工具检查工作区路径、符号链接与文件大小。命令使用参数列表执行，限制时间和输出，按白名单构造子进程环境，避免继承模型服务配置。工作区写入受 `ALLOW_WRITE` 控制。这些检查、命令护栏与资源限制不能替代操作系统隔离，也不是对 CPU、内存、磁盘或所有攻击方式的绝对保证。

Bubblewrap 不存在、平台不支持或命名空间／挂载创建失败时，命令被拒绝或返回失败，**不会自动切换到 trusted**。安装 `bwrap` 不代表内核与宿主策略允许执行；Ubuntu 的 AppArmor 和用户命名空间配置也可能影响运行。管理员应检查对应错误和系统策略，不能以关闭测试或静默降级来声称隔离成功。[Ubuntu AppArmor 文档](https://documentation.ubuntu.com/security/security-features/privilege-restriction/apparmor/)解释了这类限制。

CI 在临时 Ubuntu runner 上加载发行版的 Bubblewrap 用户命名空间策略；该策略文件不存在时，仅为 `/usr/bin/bwrap` 加载显式 `userns` 授权。它不会关闭全局 AppArmor 限制，也不会更改 Agent 的 Sandbox 参数。随后通过生产 `RunCommandTool` 实际启动 Sandbox，再运行现有文件、网络、环境与只读边界测试。策略加载或预检失败会使工作流失败。

Ubuntu 宿主若出现 `Failed RTM_NEWADDR: Operation not permitted`，应由管理员检查已有 Bubblewrap AppArmor 策略是否加载，按 [Ubuntu 用户命名空间说明](https://documentation.ubuntu.com/release-notes/23.10/#security)给予执行器适用的授权。已有其他策略时不要盲目创建重复的可执行文件匹配项。CI 的临时 runner 配置不能直接替代本机策略审查。

发行版提供 `/etc/apparmor.d/bwrap-userns-restrict` 时，可先查看策略，再由管理员加载并复验：

```bash
sudo aa-status
sudo cat /etc/apparmor.d/bwrap-userns-restrict
sudo apparmor_parser -r /etc/apparmor.d/bwrap-userns-restrict
python scripts/demo_offline.py
```

文件不存在或已有其他 Bubblewrap 策略时，管理员应按上述 Ubuntu 文档配置适用的策略，避免关闭系统级限制。成功与否以最后的实际 Smoke 结果为准。

## Trusted 与 Disabled

`--execution-mode trusted` 或 `.env` 中的 `EXECUTION_MODE=trusted` 是显式选择。代码拥有启动进程的宿主权限，能够访问该用户可访问的文件与网络。它只适用于受信代码，不能作为 Sandbox 的安全等价替代，也不能用于规避 CI 隔离失败。

`--execution-mode disabled` 禁止命令执行；禁用执行后，依赖实际运行的候选验证与质量测量也不能完成。查看已有保存案例仍不需要执行新测试或调用模型。

## Web 与模型凭据

Web 监听 `127.0.0.1`，检查 Host 与 Origin。它用于本机交互，没有公网多用户服务所需的认证、租户隔离或部署保障；不要直接开放到公网。

真实模型配置位于 `.env`，该文件被 Git 忽略。服务端调用兼容 API，日志与公开事件进行脱敏，命令子进程过滤服务凭据。这些措施不能保证所有形式的秘密都被识别：不要把真实凭据写入源码、任务、工作区文件、测试断言或公开运行记录。提交与分享前应检查文件和日志。

Saved Case 读取历史记录；Offline Demo 使用预定义模型响应并实际执行工具；Real LLM 才会请求配置的模型。无密钥演示不能自由生成新的模型测试；真实请求会使用相应服务，可能产生费用，结果与时间也可能变化。

## 测试与评价边界

当前主要支持自包含 Python 函数。契约验证处理有限、可检查的测试形式，不能完整理解任意自然语言契约。

- pytest 通过表示与参考实现一致，不证明所有预期值正确或参考实现没有缺陷。
- 覆盖率表示执行路径，不能单独代表断言质量。
- 固定故障检出只说明对相应故障集合的判别能力；超时和未知结果不能冒充确认检出。
- 精选演示、离线脚本与工程测试不能替代真实模型的总体质量对照。

指标、既有实验结论与限制见[评价说明](evaluation.md)。
