Python 标准项目实践
===
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2025-07-08%2016%3A53%3A13&color=yellowgreen&style=flat-square)

<!--END_SECTION:badge-->

<!-- TOC -->
- [GitHub Actions](#github-actions)
    - [项目发布](#项目发布)
    - [代码覆盖测试](#代码覆盖测试)
- [参考资料](#参考资料)
    - [相关文档](#相关文档)
    - [Python 项目模板](#python-项目模板)
<!-- TOC -->


## GitHub Actions

### 项目发布
> [pypa/gh-action-pypi-publish: GitHub Action, for publishing distribution files to PyPI](https://github.com/pypa/gh-action-pypi-publish)


### 代码覆盖测试
> [codecov/codecov-action: GitHub Action that uploads coverage to Codecov](https://github.com/codecov/codecov-action)

- 虽然文档说明公开仓库不需要申请申请密钥，但是可能会报错，详见：[Error: failed to properly upload](https://github.com/codecov/codecov-action/issues/598)
- 申请 `CODECOV_TOKEN`
    - 登录 [Codecov.io](https://app.codecov.io/gh)（关联 Github）；
    - 查看 `Not yet setup` 一栏（默认显示 `Enabled`），选择需要测试的仓库；
    - 将 `CODECOV_TOKEN` 添加到 [Actions secrets](#添加-actions-secrets)

示例
```yaml
steps:
- name: Checkout Repo
  uses: actions/checkout@v3
- name: Setup Python
  uses: actions/setup-python@v4
  with:
    python-version: '3.10'
- name: Install dependencies
  run: |
    python -m pip install --upgrade pip
    python -m pip install flake8 pytest pytest-cov
    pip install -r requirements.txt
- name: Setup package
    run: python setup.py install
- name: Pytest with Generate coverage report
  run: pytest --cov=<package_name> --cov-report=xml:./coverage.xml  # import <package_name>
- name: Upload coverage to Codecov
  uses: codecov/codecov-action@v3
  with:
    token: ${{ secrets.CODECOV_TOKEN }}
    flags: pytest
    directory: ./coverage/reports/
    files: ./coverage.xml
    fail_ci_if_error: true
    verbose: true
```


## 参考资料

### 相关文档
- [Quickstart - setuptools 65.3.0.post20220826 documentation](https://setuptools.pypa.io/en/latest/userguide/quickstart.html)
    > 基于 `setup.cfg` 或 `pyproject.toml` 构建 `setup.py`
- [gitignore/Python.gitignore at main · github/gitignore](https://github.com/github/gitignore/blob/main/Python.gitignore)
    > Python .gitignore 文件 


### Python 项目模板
- [yngvem/python-project-structure: A tutorial on how to manage a Python project](https://github.com/yngvem/python-project-structure)
    > 标准的 Python 项目结构（偏旧，不再维护）
- [johnthagen/python-blueprint: Example Python project using best practices](https://github.com/johnthagen/python-blueprint)
    > 基于 [poetry](https://python-poetry.org/) 构建项目
