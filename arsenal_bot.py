import os
import requests

# 从 GitHub Secrets 中安全读取密钥
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
FOOTBALL_TOKEN = os.environ.get('FOOTBALL_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

def get_arsenal_match():
    # 阿森纳 ID 为 57
    url = "https://api.football-data.org/v4/teams/57/matches?status=SCHEDULED"
    headers = {'X-Auth-Token': FOOTBALL_TOKEN}
    
    try:
        # GitHub Actions 环境不需要配置代理，直接请求即可
        response = requests.get(url, headers=headers, timeout=15)
        data = response.json()
        
        if 'matches' in data and len(data['matches']) > 0:
            match = data['matches'][0]
            home = match['homeTeam']['name']
            away = match['awayTeam']['name']
            time_str = match['utcDate'].replace('T', ' ').replace('Z', ' UTC')
            return f"📢 枪迷请注意！\n\n下一场比赛：\n🏠 {home} \nVS \n🚀 {away}\n\n📅 时间: {time_str}"
    except Exception as e:
        return f"❌ 查询比赛出错: {e}"
    return "⚽ 暂时没有查到阿森纳的比赛安排。"

def send_telegram_msg(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    try:
        requests.post(url, data=payload, timeout=15)
    except Exception as e:
        print(f"❌ 发送消息失败: {e}")

if __name__ == "__main__":
    content = get_arsenal_match()
    send_telegram_msg(content)
    print("程序运行结束！")
