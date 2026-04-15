# DOCX Replacer Service

A simple Flask API that replaces `{{PLACEHOLDER}}` tags in Word documents.

## Endpoint

`POST /replace`

- `file`: the .docx file (multipart form)
- Any additional form fields are used as replacements

## Example

```
POST /replace
Content-Type: multipart/form-data

file: template.docx
NACHNAME: Mustermann
VORNAME: Max
EMAIL: max@example.com
```

Returns the filled .docx file.
