import requests
import re
from packaging import version  # 需要安装：pip install packaging

# 配置信息
REPO_OWNER = "Fanzecheng"  # GitHub仓库所有者
REPO_NAME = "Surveillant"  # 仓库名称
LOCAL_VERSION_FILE = "version.txt"  # 本地版本存储文件
GITHUB_API_URL = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/releases/latest"  # GitHub API地址


def get_local_version():
    """获取本地版本号"""
    try:
        with open(LOCAL_VERSION_FILE, "r") as f:
            return f.read().strip()  # 读取并去除空白字符
    except FileNotFoundError:
        print("⚠️ 未找到版本文件，使用默认版本 0.0.0")
        return "0.0.0"  # 默认版本


def get_latest_release():
    """从GitHub获取最新发布信息"""
    try:
        response = requests.get(GITHUB_API_URL, timeout=10)  # 10秒超时
        response.raise_for_status()  # 检查HTTP错误
        return response.json()  # 返回JSON格式的数据
    except requests.RequestException as e:
        print(f"🚫 获取发布信息失败: {e}")
        return None


def update_available(local_ver, remote_ver):
    """检查是否有可用更新"""
    try:
        # 使用专业的版本号比较库
        return version.parse(local_ver) < version.parse(remote_ver)
    except Exception:
        # 备用方案：字符串比较
        return local_ver < remote_ver


def main():
    print("🔍 正在检查更新...")

    # 获取本地版本
    local_version = get_local_version()
    print(f"  当前本地版本: v{local_version}")

    # 获取远程版本信息
    release_info = get_latest_release()
    if not release_info:
        print("❌ 无法获取更新信息，请检查网络连接")
        return

    # 提取版本号（移除可能的'v'前缀）
    remote_version = release_info['tag_name'].lstrip('v')
    release_url = release_info['html_url']
    print(f"  最新远程版本: v{remote_version}")

    # 检查更新
    if update_available(local_version, remote_version):
        print("\n" + "=" * 50)
        print(f"✨ 发现新版本! v{local_version} → v{remote_version}")
        print(f"📥 下载地址: {release_url}")
        print("=" * 50)

        # 可选：自动下载更新包
        # for asset in release_info.get('assets', []):
        #     if asset['name'].endswith('.zip'):
        #         download_asset(asset['browser_download_url'])
    else:
        print("\n✅ 当前已是最新版本!")


if __name__ == "__main__":
    main()