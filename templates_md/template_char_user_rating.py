


def dos():
    return f'''
```chartsview
#-----------------#
#- chart type    -#
#-----------------#
type: Column

#-----------------#
#- chart data    -#
#-----------------#
data:
   - folder: "PIECE OF CAKE"
    count: {int(user_rating["1"]["user"]) + int(user_rating["1"]["root"])}
    
   - folder: "VERY EASY"
    count: {int(user_rating["2"]["user"]) + int(user_rating["2"]["root"])}

   - folder: "EASY"
    count: {int(user_rating["3"]["user"]) + int(user_rating["3"]["root"])}
    
   - folder: "NOT TO EASY"
    count: {int(user_rating["4"]["user"]) + int(user_rating["4"]["root"])}
    
   - folder: "MEDIUM"
    count: {int(user_rating["5"]["user"]) + int(user_rating["5"]["root"])}
    
   - folder: "A BIT HARD"
    count: {int(user_rating["6"]["user"]) + int(user_rating["6"]["root"])}
    
   - folder: "HARD"
    count: {int(user_rating["7"]["user"]) + int(user_rating["7"]["root"])}
    
   - folder: "EXTREMELY HARD"
    count: {int(user_rating["8"]["user"]) + int(user_rating["8"]["root"])}
    
   - folder: "INSANE"
    count: {int(user_rating["9"]["user"]) + int(user_rating["9"]["root"])}
    
   - folder: "BRAINFUCK"
    count: {int(user_rating["10"]["user"]) + int(user_rating["10"]["root"])}

#-----------------#
#- chart options -#
#-----------------#
options:
xField: "folder"
yField: "count"
padding: auto
label:
    position: "middle"
    style:
    opacity: 0.6
    fontSize: 12
columnStyle:
    fillOpacity: 0.5
    lineWidth: 1
    strokeOpacity: 0.7
    shadowColor: "grey"
    shadowBlur: 10
    shadowOffsetX: 5
    shadowOffsetY: 5
xAxis:
    label:
    autoHide: false
    autoRotate: true
meta:
    count:
    alias: "Votes"
```
'''


def get_template_char_user_rating(user_rating):
    return f'''
```chartsview
#-----------------#
#- chart type    -#
#-----------------#
type: Column

#-----------------#
#- chart data    -#
#-----------------#
data:
    - folder: "PIECE OF CAKE"
      count: {int(user_rating["1"]["user"]) + int(user_rating["1"]["root"])}
     
    - folder: "VERY EASY"
      count: {int(user_rating["2"]["user"]) + int(user_rating["2"]["root"])}

    - folder: "EASY"
      count: {int(user_rating["3"]["user"]) + int(user_rating["3"]["root"])}
      
    - folder: "NOT TO EASY"
      count: {int(user_rating["4"]["user"]) + int(user_rating["4"]["root"])}
      
    - folder: "MEDIUM"
      count: {int(user_rating["5"]["user"]) + int(user_rating["5"]["root"])}
     
    - folder: "A BIT HARD"
      count: {int(user_rating["6"]["user"]) + int(user_rating["6"]["root"])}
      
    - folder: "HARD"
      count: {int(user_rating["7"]["user"]) + int(user_rating["7"]["root"])}
      
    - folder: "EXTREMELY HARD"
      count: {int(user_rating["8"]["user"]) + int(user_rating["8"]["root"])}
      
    - folder: "INSANE"
      count: {int(user_rating["9"]["user"]) + int(user_rating["9"]["root"])}
      
    - folder: "BRAINFUCK"
      count: {int(user_rating["10"]["user"]) + int(user_rating["10"]["root"])}

    

#-----------------#
#- chart options -#
#-----------------#
options:
  xField: "folder"
  yField: "count"
  padding: auto
  label:
    position: "middle"
    style:
      opacity: 0.6
      fontSize: 12
  columnStyle:
    fillOpacity: 0.5
    lineWidth: 1
    strokeOpacity: 0.7
    shadowColor: "grey"
    shadowBlur: 10
    shadowOffsetX: 5
    shadowOffsetY: 5
  xAxis:
    label:
      autoHide: false
      autoRotate: true
  meta:
    count:
      alias: "Votes"
```
'''