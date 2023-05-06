if __name__ == "__main__":
    from graphql_app.schema import schema

    sdl = schema.as_str()

    with open("schema.graphql", "w") as f:
        f.write(sdl)
