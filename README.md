# BitBucket OAuth Migration Demo

This demo application showcases the migration path from OAuth 1.0a to OAuth 2.0 using BitBucket as an example. It demonstrates enterprise authentication scenarios and features both legacy and modern authentication methods.
![image](https://github.com/user-attachments/assets/3efabb06-f360-43aa-92a7-ddcff0aa4988)


## Features

- BitBucket authentication comparing both protocols:
  - Legacy OAuth 1.0a implementation (current Authomatic)
  - Modern OAuth 2.0 implementation (Atlassian Cloud)
- Repository access demonstration showing:
  - Basic workspace information
  - Repository listing and access
  - User permissions and scopes
- Enterprise features showcase:
  - Workspace-level authentication
  - Repository access control
  - Team membership validation

## Requirements

- Python 3.9+
- Redis server
- BitBucket OAuth credentials (both 1.0a and 2.0)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Faakhir30/authomatic-bitbucket-demo
cd authomatic-bitbucket-demo
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your BitBucket credentials and settings
```

5. Start Redis:
```bash
docker-compose up -d redis
```

## Running the Application

Start the development server:
```bash
python run.py
```

The application will be available at http://localhost:8000

## Configuration

The following environment variables are required:

### BitBucket OAuth 1.0a (Legacy)
- `BB_KEY_LEGACY`: Your legacy OAuth consumer key
- `BB_SECRET_LEGACY`: Your legacy OAuth consumer secret

### BitBucket OAuth 2.0
- `BB_CLIENT_ID`: Your OAuth 2.0 client ID
- `BB_CLIENT_SECRET`: Your OAuth 2.0 client secret
- `BB_WORKSPACE`: Your BitBucket workspace slug

### Application Settings
- `SECRET_KEY`: Application secret key
- `DEBUG`: Enable debug mode (True/False)
- `HOST`: Application host (default: localhost)
- `PORT`: Application port (default: 8000)
- `REDIS_URL`: Redis connection URL (default: redis://localhost:6379)

## API Endpoints

### Authentication
- `GET /login/bitbucket_legacy`: Initiate OAuth 1.0a authentication
- `GET /login/bitbucket_modern`: Initiate OAuth 2.0 authentication

### BitBucket Data (OAuth 2.0 only)
- `GET /api/repositories`: List repositories in workspace
- `GET /api/workspace`: Get workspace information
- `GET /api/permissions`: Get user permissions for workspace

## License

MIT License
