import requests



r = requests.get('https://datasets-server.huggingface.co/first-rows?dataset=ServiceNow%2Finsight_bench&config=default&split=train')
r.json();

