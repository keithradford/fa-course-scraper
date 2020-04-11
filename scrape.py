import argparse
import re
import requests

from lxml import html

recert_flag = False
namespaces = {"re": "http://exslt.org/regular-expressions"}

def get_html(url):
	"""Make a request to the given URL and return the HTML content"""
	content = requests.get(url)
	tree = html.fromstring(content.text)
	return tree

def filter_urls(l):
	"""Filter out any PDFs and duplicates in lists"""
	tmp = [x for x in l if not re.search(r".*(\.[Pp][Dd][Ff])$", x)]
	tmp = list(set(tmp))
	return tmp

def find_course(course, location):
	global namespaces
	global recert_flag

	ns = {"re": "http://exslt.org/regular-expressions"}
	fa_pattern = 'first(-|\s)?aid\s*courses?'
	course_xpath = '//*[re:match(text(), "' + fa_pattern + '", "i")]/parent::div//a[re:match(., "' + course + '", "i")]/@href'
	# print(course_xpath)
	tree = get_html('https://www.alertfirstaid.com/first-aid-course.php')
	course_url = tree.xpath(course_xpath, namespaces = namespaces)
	print(course_url)
	tree = get_html(course_url[0])
	if recert_flag:
		course_url = tree.xpath('//*[re:match(., "' + location + '", "i") and re:match(., "schedule", "i") and re:match(., "recert", "i")]/a/@href', namespaces = namespaces)
	else:
		course_url = tree.xpath('//*[re:match(., "' + location + '", "i") and re:match(., "schedule", "i") and not(re:match(., "recert", "i"))]/a/@href', namespaces = namespaces)

	course_url = filter_urls(course_url)

	recerts = []
	for url in course_url:
		tree = get_html(url)
		date = tree.xpath("//*[contains(@id, 'Recert')]/following-sibling::table//tr")
		for recert in date:
			recert = recert.text_content()
			recert = " ".join(recert.split())
			recert = recert.replace('\n', '')
			recert = recert.replace('\r', '')
			recerts.append(recert)
	filter_object = filter(lambda x: x != "", recerts)
	recerts = list(filter_object)
	print(recerts)



def main():
	global recert_flag

	parser = argparse.ArgumentParser(description='Find a first-aid course.')
	parser.add_argument('-c', '--course', type=str, action='store', nargs='*', help='Name of the first-aid course.')
	parser.add_argument('-l', '--location', type=str, action='store', nargs='*', help='Location of the first-aid course.')
	parser.add_argument('-r', '--recert', action='store_true', help='If the course is a recertification.')
	args = parser.parse_args()

	loc = args.location[0]
	course = args.course[0]

	if args.recert:
		recert_flag = True
	find_course(course, loc)

if __name__ == '__main__':
	main()