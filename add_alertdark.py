p='static/css/style.css'
s=open(p).read()
add='''

.alert-dark {
  background: #000000;
  border-color: #000000;
  color: #FFFFFF;
}
'''
s=s.rstrip()+'\n'+add
open(p,'w').write(s)
print('done')
"