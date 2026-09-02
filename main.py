import os

import uvicorn


def main() -> None:
    uvicorn.run(
        "web_app:app",
        host=os.getenv("HOST", "127.0.0.1"),
        port=int(os.getenv("PORT", "8080")),
        reload=False,
    )


if __name__ == "__main__":
    main()
