import io
import zipfile

import main
from make_pdf import make_pdf


def up(client, name, data):
    return client.post("/api/extract", params={"name": name}, content=data, headers={"content-type": "application/octet-stream"})


def test_txt(client):
    r = up(client, "notes.txt", "héllo\nworld".encode())
    assert r.status_code == 200 and r.json()["text"] == "héllo\nworld"


def test_md_uppercase_extension_and_bom(client):
    r = up(client, "n.MD", b"\xef\xbb\xbf# Title\n- a")
    assert r.status_code == 200 and r.json()["text"].startswith("# Title")


def test_markdown_extension(client):
    assert up(client, "n.markdown", b"x").status_code == 200


def test_docx(client):
    doc = ('<?xml version="1.0"?><w:document xmlns:w="x"><w:body>'
           '<w:p><w:pPr><w:pStyle w:val="H"/></w:pPr><w:r><w:t>Hosting &amp; servers</w:t></w:r></w:p>'
           '<w:p/><w:p><w:r><w:t xml:space="preserve">Second </w:t></w:r><w:r><w:tab/><w:t>para</w:t></w:r></w:p>'
           '<w:tbl><w:tr><w:tc><w:p><w:r><w:t>cell</w:t></w:r></w:p></w:tc></w:tr></w:tbl>'
           '</w:body></w:document>')
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.writestr("word/document.xml", doc)
    r = up(client, "a.docx", buf.getvalue())
    assert r.status_code == 200 and r.json()["text"] == "Hosting & servers\nSecond para\ncell"


def test_corrupt_docx(client):
    assert up(client, "bad.docx", b"not a zip").status_code == 422


def test_pdf(client):
    r = up(client, "a.pdf", make_pdf("Hello PDF world"))
    assert r.status_code == 200 and "Hello PDF world" in r.json()["text"]


def test_corrupt_pdf(client):
    assert up(client, "bad.pdf", b"nope").status_code == 422


def test_textless_pdf_explains_scanned(client):
    r = up(client, "scan.pdf", make_pdf(""))
    assert r.status_code == 422 and "scanned" in r.json()["detail"]


def test_unsupported_type_lists_accepted(client):
    r = up(client, "a.exe", b"x")
    assert r.status_code == 415 and ".pdf" in r.json()["detail"]


def test_blank_file(client):
    assert up(client, "e.txt", b"   \n ").status_code == 422


def test_too_many_characters(client):
    r = up(client, "big.txt", b"a" * (main.MAX_TEXT + 1))
    assert r.status_code == 413 and "limit" in r.json()["detail"]


def test_too_many_bytes(client):
    assert up(client, "huge.txt", b"a" * (main.MAX_UPLOAD + 1)).status_code == 413
