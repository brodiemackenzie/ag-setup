# Technical Design: Submission Form

## 1. Data Models & Schemas
### Database File: `guestbook.json`
Array of objects:
```json
[
  {
    "name": "Jane Doe",
    "comment": "Had an amazing weekend in the nature reserve!",
    "timestamp": "2026-06-08T12:00:00Z",
    "generated_comment": "Glad nature recharged you! Hope you didn't get chased by squirrels!",
    "image_path": "/static/images/jane_doe_17178888.png"
  }
]
```

## 2. API & Integration Contracts
### GET /
Renders index.html showing submission form and past guest entries.

### POST /submit
Parameters (Form POST): `name`, `comment`.
Calls Vertex AI Gemini and Imagen, saves image to `static/images/`, appends entry to `guestbook.json`, and redirects to `/`.

## 3. Verification Strategy
* Unit/Integration Tests (`tests/test_app.py`):
  * `test_home_page`: GET `/` returns 200.
  * `test_valid_submission`: POST `/submit` with valid parameters returns 302 redirect.
  * Mocks: Mock the `google.genai.Client` text and image generation calls to return stable mock responses and dummy image bytes, allowing hermetic offline testing.
