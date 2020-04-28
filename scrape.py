import argparse
import re
import requests

from lxml import html

# '//*[re:match(text(), "' + fa_pattern + '", "i")]/parent::div//a[re:match(., "' + course + '", "i")]/@href' - course_xpath, var course is from cmd line
#'first(-|\s)?aid\s*courses?' - fa_pattern
# 'https://www.alertfirstaid.com/first-aid-course.php' ^^^^^
# '//*[re:match(., "' + location + '", "i") and re:match(., "schedule", "i") and re:match(., "recert", "i")]/a/@href' - links to courses (recert)
# '//*[re:match(., "' + location + '", "i") and re:match(., "schedule", "i") and not(re:match(., "recert", "i"))]/a/@href' - links to courses
# "//*[contains(@id, 'Recert')]/following-sibling::table//tr" - courses from table

recert_flag = False
namespaces = {"re": "http://exslt.org/regular-expressions"}


def get_html(frl):
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
