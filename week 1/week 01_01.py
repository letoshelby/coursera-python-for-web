# Задание по программированию: Практика по requests

import requests
import datetime


ACCESS_TOKEN = '17da724517da724517da72458517b8abce117da17da72454d235c274f1a2be5f45ee711'


def get_info(uid):
	# получаем id пользователя
	payload = {'access_token': ACCESS_TOKEN, 'user_ids': uid}
	get_id = 'https://api.vk.com/method/users.get?v=5.71&access_token=[token]&user_ids=[user_id]'
	r = requests.get(get_id, params=payload)

	# получаем список друзей пользователя
	get_friends = 'https://api.vk.com/method/friends.get?v=5.71&access_token=[token]&user_id=[user_id]&fields=bdate'
	user_id = r.json()['response'][0]['id']
	payload_friends = {'access_token': ACCESS_TOKEN, 'user_id': user_id}
	friends_req = requests.get(get_friends, params=payload_friends)

	return friends_req.json()  # возвращаем словарем


def calc_age(uid):
	friends = get_info(uid)
	count = friends['response']['count']
	data = friends['response']['items']

	now = datetime.datetime.now()
	years = []

	for friend in range(count):  # проходим по всем друзьям, получаем только тех у кого есть полная дата
		if 'bdate' in data[friend] and len(data[friend]['bdate'].split('.')) == 3:
			value = data[friend]['bdate'].split('.')
			new = now.year - int(value[2])
			years.append(new)

	viewed, calculated = [], []

	for age in years:  # создаем список из нужных нам кортежей (возраст, кол-во друзей с таким возрастом)
		if age not in viewed:
			quantity = years.count(age)
			viewed.append(age)
			calculated.append((age, quantity))

	return sorted(calculated, key=lambda key: (key[1], -key[0]), reverse=True)  # сортируем по 2-ум ключам


if __name__ == '__main__':
	res = calc_age('reigning')
	print(res)
