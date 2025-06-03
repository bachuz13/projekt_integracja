from fastapi import APIRouter, HTTPException, UploadFile, File, Query
from fastapi.responses import StreamingResponse
from app.database import client
import io
import json
import yaml
import xml.etree.ElementTree as ET
from xml.dom import minidom
import re
import xml.sax.saxutils as saxutils
from bson import ObjectId, Decimal128
from datetime import datetime

router = APIRouter()

@router.post("/import/{collection_name}")
async def import_collection(
    collection_name: str,
    file: UploadFile = File(...),
    format: str = Query(default="json", enum=["json", "yaml", "xml"])
):
    """
    Import danych do kolekcji w formacie JSON, YAML lub XML.
    """
    content = await file.read()
    try:
        if format == "json":
            data = json.loads(content)
        elif format == "yaml":
            data = yaml.safe_load(content)
        elif format == "xml":
            data = parse_xml(content)
        else:
            raise HTTPException(status_code=400, detail="Nieobsługiwany format importu.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Błąd dekodowania pliku: {e}")

    if isinstance(data, dict):
        data = [data]
    if not isinstance(data, list):
        raise HTTPException(status_code=400, detail="Niepoprawny format danych.")

    collection = client["integracja"][collection_name]
    await collection.insert_many(data)
    return {"message": f"Zaimportowano {len(data)} rekordów."}

@router.get("/export/{collection_name}")
async def export_collection(
    collection_name: str,
    format: str = Query(default="json", enum=["json", "yaml", "xml"])
):
    """
    Eksport danych z wybranej kolekcji w formacie JSON, YAML lub XML.
    """
    collection = client["integracja"][collection_name]
    data = await collection.find().to_list(length=None)

    # Usuwamy _id dla eksportu
    for doc in data:
        doc.pop("_id", None)

    if format == "json":
        json_str = json.dumps(data, indent=2, ensure_ascii=False)
        return StreamingResponse(
            iter([json_str]),
            media_type="application/json",
            headers={"Content-Disposition": f"attachment; filename={collection_name}.json"}
        )

    elif format == "yaml":
        yaml_str = yaml.dump(data, allow_unicode=True)
        return StreamingResponse(
            iter([yaml_str]),
            media_type="application/x-yaml",
            headers={"Content-Disposition": f"attachment; filename={collection_name}.yaml"}
        )

    elif format == "xml":
        try:
            root = ET.Element("data")
            for item in data:
                item_elem = ET.SubElement(root, "item")
                for key, value in item.items():
                    try:
                        safe_key = sanitize_xml_tag(key) or "unknown_field"
                        sub_elem = ET.SubElement(item_elem, safe_key)
                        escaped_value = sanitize_xml_value(value)
                        sub_elem.text = escaped_value
                    except Exception as e:
                        print(f"Błąd w polu '{key}': {e}")
                        error_elem = ET.SubElement(item_elem, "error")
                        error_elem.text = f"Error processing key '{key}': {e}"

            xml_bytes = ET.tostring(root, encoding='utf-8')
            xml_str = minidom.parseString(xml_bytes.decode("utf-8")).toprettyxml(indent="  ")
            return StreamingResponse(
                iter([xml_str]),
                media_type="application/xml",
                headers={"Content-Disposition": f"attachment; filename={collection_name}.xml"}
            )
        except Exception as e:
            print(f"Błąd eksportu XML: {e}")
            raise HTTPException(status_code=500, detail=f"Błąd eksportu XML: {e}")

    else:
        raise HTTPException(status_code=400, detail="Nieobsługiwany format eksportu.")

def parse_xml(content):
    """
    Pomocnicza funkcja do parsowania XML na listę słowników.
    """
    try:
        root = ET.fromstring(content)
        records = []
        for item_elem in root.findall("item"):
            record = {}
            for child in item_elem:
                record[child.tag] = child.text
            records.append(record)
        return records
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Błąd parsowania XML: {e}")

def sanitize_xml_tag(tag):
    """
    Zamienia spacje, średniki i polskie znaki na bezpieczne identyfikatory XML.
    """
    tag = re.sub(r"\s+", "_", tag)
    tag = re.sub(r"[;]", "_", tag)
    tag = re.sub(r"[^\w\-\.]", "", tag)
    if tag and tag[0].isdigit():
        tag = f"field_{tag}"
    return tag

def sanitize_xml_value(value):
    """
    Zamienia None na pusty string, escapuje XML, usuwa niedozwolone znaki.
    Obsługuje listy, dict oraz typy BSON (ObjectId, Decimal128, datetime).
    """
    try:
        if value is None:
            return ""
        if isinstance(value, ObjectId):
            text = str(value)
        elif isinstance(value, Decimal128):
            text = str(value.to_decimal())
        elif isinstance(value, datetime):
            text = value.isoformat()
        elif isinstance(value, list):
            text = ", ".join(str(item) for item in value)
        elif isinstance(value, dict):
            text = json.dumps(value, ensure_ascii=False)
        else:
            text = str(value)
        text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', text)
        return saxutils.escape(text)
    except Exception as e:
        print(f"Błąd w wartości '{value}': {e}")
        return f"Error: {e}"
