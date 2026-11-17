p='templates/base.html'
s=open(p).read()
old="""<li class="nav-item">
            <a class="nav-link rp-nav-premium-item {% if request.resolver_match.url_name == 'services' %}rp-nav-premium-active{% endif %}" href="{% url 'downloader:services' %}">
              <span>{{ _("Services") }}</span>
            </a>
          </li>"""
assert old in s
s=s.replace(old,'')
open(p,'w').write(s)
print('done')