#!/usr/bin/env python3
# 標準ライブラリのみの最小Python Webアプリ（BMI計算機）
import os
from wsgiref.simple_server import make_server
from urllib.parse import parse_qs

def bmi_judge(bmi):
    """BMIの簡易判定"""
    if bmi < 18.5:
        return "低体重"
    elif bmi < 25:
        return "普通体重"
    elif bmi < 30:
        return "肥満（1度）"
    elif bmi < 35:
        return "肥満（2度）"
    elif bmi < 40:
        return "肥満（3度）"
    else:
        return "肥満（4度）"

def application(environ, start_response):
    query = parse_qs(environ.get("QUERY_STRING", ""))

    height = query.get("height", [""])[0]
    weight = query.get("weight", [""])[0]

    bmi = ""
    result = ""
    error = ""

    if height or weight:
        try:
            h = float(height)
            w = float(weight)
            if h <= 0:
                raise ValueError

            h_m = h / 100
            bmi_value = w / (h_m ** 2)
            bmi = f"{bmi_value:.2f}"
            result = bmi_judge(bmi_value)

        except Exception:
            error = "入力値が不正です（数値を入力してください）"

    html = f"""
<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<title>BMI計算機</title>
<style>
body {{
    font-family: sans-serif;
    padding:40px;
    background:#f5f5f5;
}}
.container {{
    background:white;
    padding:30px;
    border-radius:10px;
    max-width:420px;
}}
h1 {{
    margin-top:0;
}}
input {{
    padding:8px;
    margin:5px 0;
    width:100%;
}}
button {{
    padding:8px 16px;
    margin-top:10px;
}}
.result {{
    margin-top:20px;
    font-size:1.2em;
    color:#0a7;
}}
.error {{
    margin-top:20px;
    color:red;
}}
</style>

<script>
function clearForm(){{
    document.getElementById("height").value="";
    document.getElementById("weight").value="";
}}
</script>

</head>
<body>

<div class="container">
<h1>BMI計算機</h1>

<form method="get">
<label>身長 (cm)</label>
<input id="height" name="height" value="{height}" placeholder="例: 170">

<label>体重 (kg)</label>
<input id="weight" name="weight" value="{weight}" placeholder="例: 65">

<button type="submit">計算</button>
<button type="button" onclick="clearForm()">クリア</button>
</form>

{f'<div class="result">BMI: {bmi}<br>判定: {result}</div>' if bmi else ''}
{f'<div class="error">{error}</div>' if error else ''}

</div>

</body>
</html>
"""

    body = html.encode("utf-8")

    start_response(
        "200 OK",
        [
            ("Content-Type", "text/html; charset=utf-8"),
            ("Content-Length", str(len(body)))
        ]
    )
    return [body]


if __name__ == "__main__":
    # Render / ローカル共通
    port = int(os.environ.get("PORT", 8000))
    with make_server("0.0.0.0", port, application) as httpd:
        print(f"Serving on http://0.0.0.0:{port}")
        httpd.serve_forever()