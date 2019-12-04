import requests
privateToken = 'kSeX-psAkxw3NGBabgUy'
privateTokenStr = 'private_token={}'.format(privateToken)
projectId = 15617391
prefix = 'https://gitlab.com/api/v4/projects/{}'.format(projectId)

categories = [
	{

		"label": {
            "id": "Journal Account",
			"name": "journal-account",
			"color": "#3450f6"
		},
        "label":{
            "id":"Patient Account",
            "name": "patient-account",
            "color": "#3450f6"
        }
	}
]

for category in categories:
	label = category.get('label')
	resp = requests.post('{}/labels?{}'.format(prefix, privateTokenStr), json = label)
	if resp.status_code != 201:
		if resp.status_code != 409: # Label already exists
			raise Exception('POST /labels/: {} - {}'.format(resp.status_code, resp.text))

resp = requests.get('{}/issues?{}'.format(prefix, privateTokenStr))
if resp.status_code != 201:
		raise Exception('GET /issues/: {} - {}'.format(resp.status_code, resp.text))

jsonResp = resp.json()
if not isinstance(jsonResp, list):
	jsonResp = [jsonResp]

for issue in jsonResp:
    title = issue.get('title')
    serviceDeskStr = 'Service Desk'
    if serviceDeskStr in title:
        for category in categories:
            tag = '[{}]'.format(category.get('id'))
            if tag in title:
                label = category.get('label')
                issueIid = issue.get('id')
                labelName = label.get('name')
                assignLabels = issue.get('labels')
                if not labelName in assignLabels:
                    assignLabels.append(label.get('name'))
                    updateData = { "labels": assignLabels }
                    resp = requests.put('{}/issues/{}?{}'.format(prefix,
					issueIid, privateTokenStr), json=updateData)
                    if resp.status_code != 200:
                        raise Exception('PUT /issues/{}/: {} - {}'.format(issueIid,
						resp.status_code, resp.text))