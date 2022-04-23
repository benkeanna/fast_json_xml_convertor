xml_string = """
<ITEM type="object"> 
    <ITEM key="apple" type="integer" value="7"/>
    <ITEM key="orange" type="float" value="4.1"/>
    <ITEM key="other" type="object">                                   
        <ITEM key="banana" type="string" value="fruit"/>
    </ITEM> 
    <ITEM key="many" type="list"> 
        <ITEM type="boolean" value="true"/>
        <ITEM type="string" value="thing"/>
        <ITEM type="object"> 
            <ITEM key="pineapple" type="null"/>
        </ITEM> 
    </ITEM> 
</ITEM> """


json_string = """
{ 
  "apple": 7,
  "orange": 4.1,
  "other": {
    "banana": "fruit"
  },
  "many": [
    true,
    "thing",
      {
      "pineapple": null
      }
  ]
}"""
