#!/usr/bin/env python3
"""
测试QQ邮箱发送功能
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

def test_email_send(email_from, email_password, email_to):
    """测试邮件发送"""
    print("🔧 测试QQ邮箱发送功能...")
    print(f"发送邮箱: {email_from}")
    print(f"目标邮箱: {email_to}")
    
    # 创建邮件
    today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f"🎵 Discogs邮件发送测试 - {today}"
    msg['From'] = email_from
    msg['To'] = email_to
    
    # 邮件内容
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; padding: 20px; }}
            .header {{ background: #4a6fa5; color: white; padding: 20px; text-align: center; }}
            .content {{ padding: 20px; background: #f9f9f9; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🎵 Discogs邮件发送测试</h1>
            <p>测试时间: {today}</p>
        </div>
        <div class="content">
            <h2>✅ 邮件发送测试成功！</h2>
            <p>如果你的Discogs任务配置正确，明天10:00你会收到类似这样的邮件：</p>
            <ul>
                <li>最新House音乐推荐</li>
                <li>音乐标题和艺术家信息</li>
                <li>Discogs直接链接</li>
                <li>精美的HTML格式</li>
            </ul>
            <p><strong>今日测试音乐:</strong> Pet Shop Boys - Introspective</p>
            <p><strong>Discogs链接:</strong> https://www.discogs.com/release/23360639</p>
        </div>
    </body>
    </html>
    """
    
    msg.attach(MIMEText(html_content, 'html'))
    
    try:
        # QQ邮箱SMTP配置
        smtp_server = "smtp.qq.com"
        smtp_port = 587
        
        print("正在连接QQ邮箱SMTP服务器...")
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            print("正在登录邮箱...")
            server.login(email_from, email_password)
            print("正在发送测试邮件...")
            server.send_message(msg)
        
        print(f"✅ 测试邮件已成功发送到 {email_to}")
        return True
        
    except Exception as e:
        print(f"❌ 邮件发送失败: {str(e)}")
        return False

def main():
    """主函数"""
    print("="*60)
    print("📧 Discogs邮件发送功能测试")
    print("="*60)
    
    # 从用户输入获取邮箱信息
    print("\n请输入以下信息进行测试：")
    
    email_from = input("1. 发送邮箱 (如: 12345678@qq.com): ").strip()
    if not email_from:
        print("❌ 发送邮箱不能为空")
        return
    
    email_password = input("2. 邮箱授权码 (不是QQ密码): ").strip()
    if not email_password:
        print("❌ 邮箱授权码不能为空")
        return
    
    email_to = "3897451169@qq.com"
    
    print(f"\n📋 测试配置：")
    print(f"   发送邮箱: {email_from}")
    print(f"   目标邮箱: {email_to}")
    
    # 测试发送
    success = test_email_send(email_from, email_password, email_to)
    
    if success:
        print("\n🎉 测试成功！")
        print("请检查你的邮箱 3897451169@qq.com 是否收到测试邮件。")
        print("\n🔧 接下来需要配置定时任务：")
        print(f"1. 编辑配置文件: nano /root/.openclaw/workspace/scripts/run_discogs.sh")
        print(f"2. 修改以下行：")
        print(f'   export EMAIL_FROM="{email_from}"')
        print(f'   export EMAIL_PASSWORD="{email_password}"')
        print(f"3. 保存并退出")
        print(f"\n📅 配置完成后，明天10:00会自动收到Discogs音乐推荐邮件。")
    else:
        print("\n❌ 测试失败，请检查：")
        print("1. QQ邮箱是否正确")
        print("2. 是否开启了SMTP服务")
        print("3. 授权码是否正确（不是QQ密码）")
        print("4. 网络连接是否正常")

if __name__ == "__main__":
    main()