import os
import requests

# 保持 Secret 读取部分不变
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
FOOTBALL_TOKEN = os.environ.get('FOOTBALL_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

def get_arsenal_match():
    # 修改这里的 URL，获取该球队所有赛事的赛程
    url = "https://api.football-data.org/v4/teams/57/matches"
    headers = {'X-Auth-Token': FOOTBALL_TOKEN}
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        data = response.json()
        
        if 'matches' in data and len(data['matches']) > 0:
            # 我们只筛选“未开始”的比赛 (SCHEDULED 或 TIMED)
            upcoming = [m for m in data['matches'] if m['status'] in ['SCHEDULED', 'TIMED']]
            
            if not upcoming:
                return "⚽ 暂时没有查到阿森纳后续的比赛安排。"

            # 取最近的一场
            match = upcoming[0]
            home = match['homeTeam']['name']
            away = match['awayTeam']['name']
            comp = match['competition']['name'] # 获取赛事名称（如 Champions League）
            
            # 时间处理
            time_str = match['utcDate'].replace('T', ' ').replace('Z', '')
            
            return (f"📢 枪迷情报站 (全赛事版)\n\n"
                    f"🏆 赛事: {comp}\n"
                    f"🏠 {home}\n"
                    f"VS\n"
                    f"🚀 {away}\n\n"
                    f"📅 时间(UTC): {time_str}\n"
                    f"💡 请注意：这是最近的一场比赛。")
                    
    except Exception as e:
        return f"❌ 查询失败: {e}"
    return "⚽ 暂时没有查到比赛安排。"

# 下面的发送函数保持不变
def send_telegram_msg(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    try:
        requests.post(url, data=payload, timeout=15)
    except Exception as e:
        print(f"❌ 发送失败: {e}")

if __name__ == "__main__":
    content = get_arsenal_match()
    send_telegram_msg(content)
