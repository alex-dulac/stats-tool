# stats-tool

A full stack web application utilizing several tools to provide users with an easy-to-use interface for browsing and comparing hockey stats on a data set.

### The project features:
- #### Client
  - Vue
  - Vuetify (Vue UI library)
  - Pinia (State management)
  - Observable Plot (built with D3.js)
- #### Server
  - FastAPI
  - PostgreSQL
  - SQLModel (SQLAlchemy + Pydantic)

### Quick start:

1. Install Docker locally.
2. In both the `client` & `server` directories, you will need to create an `.env` file from the example.
  - `cd client && cp .env.example .env && cd ..`
  - `cd server && cp .env.example .env && cd ..`
3. In the project root, run `docker compose up` (use `-d` to run in background)

#### Note:
   - To rebuild the client after adding new npm packages, run:
     - `docker compose build client && docker compose up`
   - To rebuild the server after adding new python packages, run:
     - `docker compose build server && docker compose up`

### Local Node Development
  - To run the client app without Docker, comment out the `client` service in `docker-compose.yml` and run the following commands:
    - `cd client`, `npm install`, `npm run dev`


### Access points:
- Web app: `http://localhost:5173/`
- FastAPI docs: `http://localhost:8000/docs`
- pgAdmin: `http://localhost:5050/` 
  - username: `admin@cooldemo.net`, password: `coolPassword555`
  - add a server
    - name: anything you want
    - Host name/address: `db`
    - Port: `5432`
    - Username: `postgres`
    - Password: `postgres`


