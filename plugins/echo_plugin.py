async def custom_echo(data):
    return f\"Plugin Echo: {data.upper()}\"

def register():
    return {
        \"custom_echo\": custom_echo
    }
