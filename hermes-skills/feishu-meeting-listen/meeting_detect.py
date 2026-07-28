#!/usr/bin/env python3
"""
会议检测 — 仅检测入会 + 启动 poll.sh 监听
不做 C360、不推通知、不生成纪要（交给 LLM cron）
"""
import json, os, re, subprocess, sys
from datetime import datetime, timezone, timedelta

TZ = timezone(timedelta(hours=8))
CLIENT_PATTERNS = [
    r"(.+?)\s*[xX×]\s*飞书", r"(.+?)\s*[xX×]\s*Feishu",
    r"(.+?)\s*[xX×]\s*Lark", r"(.+?)\s*[xX×]\s*AI",
    r"(.{4,12})(?:交流|沟通|拜访|签约|谈判|合作|讨论)$",
]
KNOWN_CLIENTS = [
    "零壹创新","福建电子信息","普洛德","拓竹","疆海","安克创新","致欧",
    "敦煌网","猿人","感臻","高驰","COROS","逸文","唯迹","星网锐捷",
    "雷鸟","凯特","和生","SHEIN","Temu",
]

def extract_client(title):
    for p in CLIENT_PATTERNS:
        m = re.search(p, title)
        if m:
            name = m.group(1).strip()
            if len(name) >= 3 and not name.startswith("和") and not name.startswith("与"):
                return name
    for kw in KNOWN_CLIENTS:
        if kw in title and len(kw) >= 3:
            return kw
    return None
STATE_FILE = os.path.expanduser("~/.hermes/cron/meeting_state.json")
LARK_CLI = "/Users/bytedance/.npm-global/bin/lark-cli"
POLL_SCRIPT = os.path.expanduser("~/.hermes/skills/feishu/feishu-meeting-listen/scripts/poll.sh")

def load_state():
    try:
        with open(STATE_FILE) as f:
            return json.load(f)
    except:
        return {}

def save_state(s):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, 'w') as f:
        json.dump(s, f, ensure_ascii=False, indent=2)

def run_cmd(cmd, timeout=15):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    except:
        return None

def start_poll(meeting_id, title):
    """启动 poll.sh 后台监听，返回 PID"""
    try:
        r = subprocess.run(["pgrep", "-f", f"poll.sh.*{meeting_id}"],
                           capture_output=True, text=True, timeout=5)
        if r.returncode == 0 and r.stdout.strip():
            return None  # 已在运行
    except:
        pass
    try:
        safe_title = title.replace("'", "").replace('"', "").replace("&", "")
        proc = subprocess.Popen(
            ["bash", POLL_SCRIPT, meeting_id, safe_title],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            start_new_session=True,
        )
        return proc.pid
    except:
        return None

def poll_alive(pid):
    if pid is None:
        return False
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False

def main():
    state = load_state()
    now = datetime.now(TZ).isoformat()
    now_ts = datetime.now(TZ)

    r = run_cmd([LARK_CLI, "vc", "+meeting-list-active", "--as", "user"], timeout=15)
    if not r or r.returncode != 0:
        return
    try:
        data = json.loads(r.stdout)
        meetings = data.get("data", {}).get("meetings", [])
    except:
        return

    active_ids = {m["meeting_id"] for m in meetings}

    for m in meetings:
        mid = m["meeting_id"]
        title = m.get("meeting_title", "")

        if mid not in state:
            client = extract_client(title)
            state[mid] = {"title": title, "status": "new", "first_seen": now, "pid": None, "log_size": 0, "client": client}
            pid = start_poll(mid, title)
            if pid:
                state[mid]["pid"] = pid
                state[mid]["status"] = "monitoring"
            else:
                state[mid]["status"] = "monitoring"  # 已有进程
        else:
            pid = state[mid].get("pid")
            st = state[mid].get("status", "")
            if st == "monitoring" and pid and not poll_alive(pid):
                state[mid]["status"] = "completed"
                state[mid]["completed_at"] = now
                state[mid]["pid"] = None
                logf = os.path.expanduser(f"~/meeting_logs/{mid}.jsonl")
                if os.path.exists(logf):
                    state[mid]["log_size"] = os.path.getsize(logf)
            if st == "completed":
                pass  # waiting for LLM cron

    # 不活跃的 monitoring 会议 → 检查 poll 是否退出
    for mid, info in list(state.items()):
        if info.get("status") == "monitoring" and mid not in active_ids:
            pid = info.get("pid")
            if pid and not poll_alive(pid):
                info["status"] = "completed"
                info["completed_at"] = now
                info["pid"] = None
                logf = os.path.expanduser(f"~/meeting_logs/{mid}.jsonl")
                if os.path.exists(logf):
                    info["log_size"] = os.path.getsize(logf)

    # 清理 7 天前
    cutoff = (now_ts - timedelta(days=7)).isoformat()
    state = {k: v for k, v in state.items()
             if v.get("first_seen", "") > cutoff or v.get("status") == "monitoring"}

    save_state(state)
    # 完全静默，不推送任何内容给用户

if __name__ == "__main__":
    main()
