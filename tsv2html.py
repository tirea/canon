#!/usr/bin/env python3

import bbcode  # pip3 install bbcode
from datetime import datetime


def gen_title(outfile):
	with open(outfile, "w") as html:
		html.write('<!DOCTYPE html>\n')
		html.write('<html>')
		html.write('<head>')
		html.write('<title>/language-updates</title>')
		html.write('<meta charset="utf-8">')
		html.write('</head>')
		html.write('<body>\n')
		html.write('<h1 id="top">/language-updates</h1>\n')


def gen_toc(infile, outfile):
	with open(outfile, "a") as html:
		html.write('<h2>Table of Contents</h2>\n<ul>\n')

		with open(infile) as tsv:
			index = 0
			for line in tsv:
				row = line.strip().split('\t')
				thread = row[5]
				if thread.startswith('"') and thread.endswith('"'):
					thread = thread[1:-1]
				if not thread.startswith("Re:"):
					html.write('<li><a href="#{}">{}</a></li>\n'.format(index, thread))
					index += 1
		html.write('</ul>\n')


def bbc2html(text):
	out = text

	# fix table errors
	out = out.replace('[table]<br />', '[table]').replace('<br />[/table]', '[/table]')
	out = out.replace('[tr]<br />', '[tr]').replace('<br />[/tr]', '[/tr]')
	out = out.replace('[/tr]<br />', '[/tr]')
	out = out.replace('[td]<br />', '[td]').replace('<br />[/td]', '[/td]')
	out = out.replace('[/td]<br />', '[/td]')

	# b i u s
	out = out.replace('[b]', '<strong>').replace('[/b]', '</strong>')
	out = out.replace('[i]', '<em>').replace('[/i]', '</em>')
	out = out.replace('[u]', '<u>').replace('[/u]', '</u>')
	out = out.replace('[s]', '<del>').replace('[/s]', '</del>')

	# color
	colors = ['black', 'red', 'yellow', 'pink', 'green', 'orange', 'purple', 
	'blue', 'beige', 'brown', 'teal', 'navy', 'maroon', 'limegreen', 'white']
	for color in colors:
		out = out.replace('[color={}]'.format(color), '<span style="color:{};">'.format(color))
	out = out.replace('[/color]', '</span>')

	# tables
	out = out.replace('[table]', '<table>').replace('[/table]', '</table>')
	out = out.replace('[thead]', '<thead>').replace('[/thead]', '</thead>')
	out = out.replace('[tbody]', '<tbody>').replace('[/tbody]', '</tbody>')
	out = out.replace('[tr]', '<tr>').replace('[/tr]', '</tr>')
	out = out.replace('[td]', '<td>').replace('[/td]', '</td>')

	# size
	for size in range(72):
		out = out.replace('[size={}pt]'.format(size), '<span style="font-size:{}pt;">'.format(size))
	out = out.replace('[/size]', '</span>')

	# font
	fonts = ['courier', 'arial', 'arial black', 'impact', 'verdana', 
	'times new roman', 'georgia', 'andale mono', 'trebuchet ms', 'comic sans ms']
	for font in fonts:
		out = out.replace('[font={}]'.format(font), '<span style="font-family: {};">'.format(font))
	out = out.replace('[/font]', '</span>')

	# pre left center right
	out = out.replace('[pre]', '<pre>').replace('[/pre]', '</pre>')
	out = out.replace('[left]', '<div style="text-align:left;">').replace('[/left]', '</div>')
	out = out.replace('[center]', '<div style="text-align:center;">').replace('[/center]', '</div>')
	out = out.replace('[right]', '<div style="text-align:right;">').replace('[/right]', '</div>')

	# lists
	out = out.replace('[list]', '<ul>').replace('[/list]', '</ul>')
	out = out.replace('[li]', '<li>').replace('[/li]', '</li>')

	# sub sup
	out = out.replace('[sub]', '<sub>').replace('[/sub]', '</sub>')
	out = out.replace('[sup]', '<sup>').replace('[/sup]', '</sup>')

	# code tt
	out = out.replace('[code]', '<pre style="font-family: monospace;">').replace('[/code]', '</pre>')
	out = out.replace('[tt]', '<pre style="font-family: monospace;">').replace('[/tt]', '</pre>')

	# hr
	out = out.replace('[hr]', '='*16)

	# img, url, spoiler, desc, quote, or anything else with an equals sign? nah.
	
	return out


def gen_posts(infile, outfile):
	with open(outfile, "a") as html:
		with open(infile) as tsv:
			index = 0
			for line in tsv:
				row = line.strip().split('\t')
				msg, topic, board = row[0], row[1], row[2]
				timestamp = datetime.utcfromtimestamp(int(row[3])).strftime("%Y-%m-%d %H:%M:%S")
				u, thread, username, body = row[4], row[5], row[6], row[7]

				if thread.startswith('"') and thread.endswith('"'):
					thread = thread[1:-1]
				if body.startswith('"') and body.endswith('"'):
					body = body[1:-1]

				html.write('<br><hr><br>\n')
				html.write('<a href="https://forum.learnnavi.org/?msg={}">msg={}</a>'.format(msg, msg))
				html.write(' | ')
				html.write('<a href="https://forum.learnnavi.org/?topic={}">topic={}</a>\t'.format(topic, topic))
				html.write(' | ')
				html.write('<a href="https://forum.learnnavi.org/?board={}">board={}</a>\t'.format(board, board))
				html.write(' | ')
				html.write('time={}\t'.format(timestamp))
				html.write(' | ')
				html.write('<a href="https://forum.learnnavi.org/profile/?u={}">u={}</a>\n'.format(u, u))
				if not thread.startswith("Re:"):
					html.write('<h2 id="{}">{}</h2>\n'.format(index, thread))
					index += 1
				else:
					html.write('<h2>{}</h2>\n'.format(thread))
				html.write('<h4>{}</h4>\n'.format(username))
				html.write('<div class="smf-post">\n')
				html.write('{}\n'.format(bbc2html(body)))
				html.write('</div>\n')


def gen_footer(outfile):
	with open(outfile, "a") as html:
		html.write('<br><hr><br>\n\n<a href="#top">Go to top</a>\n')
		html.write('</body></html>')


def main():
	infile = "language_updates.tsv"
	outfile = "language_updates.html"
	gen_title(outfile)
	gen_toc(infile, outfile)
	gen_posts(infile, outfile)
	gen_footer(outfile)


if __name__ == '__main__':
	main()
