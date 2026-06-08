# Functional Specification: Submission Form

## 1. Objective
Implement a guestbook web app where visitors can submit comments. For each submission, the app uses generative AI to produce a fun customized reply and an image matching the comment's tone.

## 2. User Journeys
* **Submit Guestbook Entry**: Visitor enters their name and comment, then clicks Submit. The page reloads, showing their entry along with a witty AI response and a dynamically generated image.

## 3. Requirements
* **req-form-ui**: Simple HTML form with fields for `name` and `comment`.
* **req-genai-witty-reply**: Generate a fun, customized thank you response using the Gemini API based on the user's comment.
* **req-genai-image**: Construct a fun prompt, generate an image using Imagen, save it locally in `static/images/`, and display it next to the entry.
* **req-data-storage**: Store name, timestamp, comment, generated reply, and generated image file path in `guestbook.json`.
* **req-display**: Display all past entries on the home page in reverse chronological order.
