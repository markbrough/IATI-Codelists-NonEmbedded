from lxml import etree
import unicodecsv

codelists = ["AidType", "CollaborationType", "FinanceType", "FlowType",
"Sector"]

nsmap = {"xml": "http://www.w3.org/XML/1998/namespace"}

for codelist in codelists:
    doc = etree.parse("xml/%s.xml" % codelist)
    items = doc.xpath("//codelist-item")
    
    csvfile = open("csv/%s.csv" % codelist, "wb")
    fieldnames = ["code", "name_en", "name_fr", "description_en",
    "description_fr"]
    csv = unicodecsv.DictWriter(csvfile, fieldnames)
    csv.writeheader()
    for item in items:
        name_en = item.xpath("name/narrative[not(@xml:lang)]", 
                                    namespaces=nsmap)[0].text
        name_fr = item.find("name/narrative[@xml:lang='fr']", 
                                    namespaces=nsmap).text
        if item.xpath("description"):
            description_en = item.xpath("description/narrative[not(@xml:lang)]", 
                                    namespaces=nsmap)[0].text
            description_fr = item.find("description/narrative[@xml:lang='fr']", 
                                    namespaces=nsmap).text
        else:
            descritiption_en, description_fr = "",""
            
        csv.writerow({
            "code": item.find("code").text,
            "name_en": name_en,
            "name_fr": name_fr,
            "description_en": description_en,
            "description_fr": description_fr
        })
    csvfile.close()