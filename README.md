<div align="center">
<img width="1200" height="475" alt="GHBanner" src="https://github.com/user-attachments/assets/0aa67016-6eaf-458a-adb2-6e31a0763ed6" />
</div>

# Run and deploy your AI Studio app

This contains everything you need to run your app locally.

View your app in AI Studio: https://ai.studio/apps/drive/1lSkTdhQYx9GM3m4fdS1vQ8aqdcyAwK47

## Run Locally

**Prerequisites:**  Node.js


1. Install dependencies:
   `npm install`
2. Set the `GEMINI_API_KEY` in [.env.local](.env.local) to your Gemini API key
3. Run the app:
   `npm run dev`

## Deploy on Render

This repo already includes a [render.yaml](render.yaml) Blueprint for a two-service deployment:

1. Backend API: `chronosai-api`
2. Frontend static site: `chronosai-frontend`

To deploy:

1. Push the repo to GitHub.
2. In Render, create a new Blueprint and point it at this repository.
3. Provide the backend `MONGO_URI` when Render prompts for it.
4. Let Render create the API and frontend services from [render.yaml](render.yaml).

The frontend is built with `npm ci && npm run build` and uses `VITE_API_URL` to call the Render API service.
