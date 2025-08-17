# tools/get_refresh_token_device.py
# Device Flow cho YouTube (TVs & Limited Input). Lấy refresh_token + lưu token.json

import os, json, time, sys, requests

CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID") or "<PASTE_CLIENT_ID>"
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET") or "<PASTE_CLIENT_SECRET>"
# Device Flow chỉ chấp nhận youtube / youtube.readonly (không dùng youtube.upload)
SCOPE = os.getenv("GOOGLE_SCOPE") or "https://www.googleapis.com/auth/youtube"

DEVICE_CODE_URL = "https://oauth2.googleapis.com/device/code"
TOKEN_URL = "https://oauth2.googleapis.com/token"

def main():
    # Bước 1: xin device_code + user_code
    r = requests.post(DEVICE_CODE_URL, data={
        "client_id": CLIENT_ID,
        "scope": SCOPE
    })
    r.raise_for_status()
    p = r.json()
    user_code = p["user_code"]
    verification_url = p.get("verification_url") or p.get("verification_uri") or "https://www.google.com/device"
    device_code = p["device_code"]
    interval = int(p.get("interval", 5))
    expires_in = int(p.get("expires_in", 1800))

    print("\nMỞ TRÌNH DUYỆT TẠI:", verification_url)
    print("NHẬP MÃ:", user_code)
    print("(Đang chờ bạn xác nhận trên thiết bị khác...)")

    # Bước 2: Poll token theo interval
    start = time.time()
    while True:
        if time.time() - start > expires_in:
            sys.exit("Hết hạn mã. Chạy lại script.")
        tr = requests.post(TOKEN_URL, data={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,  # Google yêu cầu khi đổi token / refresh
            "device_code": device_code,
            "grant_type": "urn:ietf:params:oauth:grant-type:device_code"
        })
        if tr.status_code == 200:
            creds = tr.json()
            break
        j = tr.json()
        err = j.get("error")
        if err == "authorization_pending":
            time.sleep(interval); continue
        if err == "slow_down":
            interval += 5; time.sleep(interval); continue
        raise SystemExit(f"Lỗi: {err} - {j.get('error_description','')}")

    tokens = {
        "access_token": creds["access_token"],
        "refresh_token": creds.get("refresh_token"),
        "expires_in": creds["expires_in"],
        "scope": creds.get("scope"),
        "token_type": creds["token_type"],
    }
    print("\n==== TOKEN INFO ====")
    print("REFRESH TOKEN:", tokens["refresh_token"])
    with open("token.json","w",encoding="utf-8") as f:
        json.dump(tokens,f,ensure_ascii=False,indent=2)
    print("Đã lưu token.json")

if __name__ == "__main__":
    main()
