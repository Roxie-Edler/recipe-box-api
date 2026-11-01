from users_service import create_app # type: ignore

app = create_app()

if __name__ == "__main__":
    app.run(port=5001, debug=True)