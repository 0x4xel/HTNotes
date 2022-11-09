def get_template_chart_radar(user_average,author):
    return f'''
```chartsview
#-----------------#
#- chart type    -#
#-----------------#
type: Radar

#-----------------#
#- chart data    -#
#-----------------#
data:
  - item: "ENUM"
    user: "user"
    score: {user_average["enum"]}
  - item: "REAL"
    user: "user"
    score: {user_average["real"]}
  - item: "CVE"
    user: "user"
    score: {user_average["cve"]}
  - item: "CUSTOM"
    user: "user"
    score: {user_average["custom"]}
  - item: "CTF"
    user: "user"
    score: {user_average["ctf"]}
  - item: "ENUM"
    user: "author"
    score: {author["enum"]}
  - item: "REAL"
    user: "author"
    score: {author["real"]}
  - item: "CVE"
    user: "author"
    score: {author["cve"]}
  - item: "CUSTOM"
    user: "author"
    score: {author["custom"]}
  - item: "CTF"
    user: "author"
    score: {author["ctf"]}

#-----------------#
#- chart options -#
#-----------------#
options:
  xField: "item"
  yField: "score"
  seriesField: "user"
  meta:
    score:
      alias: "Score"
      min: 0
      nice: true
  xAxis:
    line: null
    tickLine: null
  yAxis:
    label: false
    grid:
      alternateColor: "rgba(0, 0, 0, 0.04)"
  point: []
  area: []
```
'''