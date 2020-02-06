import json

data = json.dumps({'abd':'4146fe1wa2893e79ys'},ensure_ascii=True)

con = ["{'customer_name': '北京嘀嘀无限科技发展有限公司', 'customer_code': 20615, 'customer_shortname': '滴滴'}"]

con = ''.join(con)
#
print(con)
con = json.dumps(con,ensure_ascii=False)
print({''.join(con.replace('"','').replace('{','').replace('}',''))})