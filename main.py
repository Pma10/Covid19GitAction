import os
import requests
import datetime

def create_github_issue(data):
    token = os.environ.get('TOKEN')
    username = "Pma10"
    repository = "Covid19GitAction"
    issue_data = f"""
    [코로나19 API 업데이트 시간] {data['API']['updateTime']}

    [한국 전체]
    총 확진자 수: {data['korea']['totalCnt']}
    사망자 수: {data['korea']['deathCnt']}
    발생률: {data['korea']['qurRate']}
    일일 확진자 증가 수: {data['korea']['incDec']}

    [지역별]
    """

    for city in data.keys():
        if city not in ['API', 'korea']:
            city_data = data[city]
            issue_data += f"""
            {city_data['countryNm']} :
            총 확진자 수: {city_data['totalCnt']}
            사망자 수: {city_data['deathCnt']}
            발생률: {city_data['qurRate']}
            일일 확진자 증가 수: {city_data['incDec']}
            """

    # 이슈 생성할 URL 설정
    url = f"https://api.github.com/repos/{username}/{repository}/issues"
    # 이슈 생성 요청 보내기
    response = requests.post(url, json={"title": f"{(datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime('%Y년 %m월 %d일')} 코로나 업데이트", "body": issue_data}, headers={"Authorization": f"token {token}"})
    print(issue_data)
    # 응답 확인
    if response.status_code == 201:
        print("새로운 이슈가 성공적으로 생성되었습니다.")
    else:
        print("새로운 이슈 생성에 실패했습니다. 응답 코드:", response.status_code)

# 데이터 가져오기
def get_corona_data():
    apiKey = os.environ.get('APIKEY')
    url = f"https://api.corona-19.kr/korea/?serviceKey={apiKey}"
    print(url)
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        print("API 요청이 실패하였습니다.")
        return None

# 코드 실행
data = get_corona_data()
if data:
    create_github_issue(data)
