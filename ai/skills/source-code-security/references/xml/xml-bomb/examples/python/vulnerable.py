from flask import Flask, request, jsonify
from lxml import etree

app = Flask(__name__)

@app.post("/saml/consume")
def consume_saml():
    parser = etree.XMLParser(resolve_entities=True, load_dtd=True)
    doc = etree.fromstring(request.data, parser)
    name_id = doc.xpath("//*[local-name()='NameID']/text()")
    return jsonify({"user": name_id[0] if name_id else None})
