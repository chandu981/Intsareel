p='templates/base.html'
s=open(p).read()
old='<li><a href="{% url \'downloader:services\' %}">{{ _("Services") }}</a></li>'
s=s.replace(old,'')
open(p,'w').write(s)
print('done')